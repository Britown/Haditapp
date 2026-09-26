"""One ledger, explicit per-movement edits, and independent monthly persistence."""
from copy import deepcopy
from datetime import datetime
import io
import re
import pandas as pd
import streamlit as st
import database
from processor_v3 import summarize
from rules import FIXED, match_rule
from training_ui import active_rules, refresh_results
from workflow import merge_edits


def render():
    st.header('Movimientos del mes')
    rows = st.session_state.get('records', [])
    if not rows:
        st.info('Importa una cartola en Importar y resumen para comenzar.')
        return
    pending = sum(r['Tipo'] == 'Revisar' or r.get('Monto') is None or not r.get('Período confirmado', True) for r in rows)
    a, b, c = st.columns(3)
    a.metric('Movimientos', len(rows))
    b.metric('Por revisar', pending)
    c.metric('Revisados por ti', sum(bool(r.get('Revisado')) for r in rows))
    if st.session_state.get('month_dirty', True):
        st.warning('Cambios sin guardar. Las correcciones aplicadas se mantienen al navegar dentro del mes.')
    else:
        st.caption('Guardado a las ' + st.session_state.get('month_saved_at', ''))
    if st.button('Guardar cambios del mes', type='primary'):
        try:
            database.save_reconciliation(database.get_db(), dict(period=st.session_state.current_month_str,
                records=rows, beneficio=st.session_state.get('beneficio_aplicado', 0)))
            st.session_state.month_dirty = False
            st.session_state.month_saved_at = datetime.now().strftime('%H:%M')
            st.rerun()
        except Exception:
            st.error('No se pudo guardar. Tus cambios siguen disponibles en esta sesión; vuelve a intentarlo.')
    if st.session_state.get('last_movement_edit') and st.button('Deshacer última corrección'):
        old = st.session_state.pop('last_movement_edit')
        st.session_state.records = [old if r['id'] == old['id'] else r for r in rows]
        st.session_state.month_dirty = True
        refresh_results()
        st.session_state.edit_revision = st.session_state.get('edit_revision', 0) + 1
        st.rerun()
    if 'gmail' in st.secrets and st.button('Consultar comentarios BICE'):
        from gmail_fetcher import fetch_bice_transfers_from_gmail
        from bice_email import enrich_transfers
        try:
            with st.spinner('Consultando comentarios BICE…'):
                emails = fetch_bice_transfers_from_gmail(st.session_state.current_month_str)
            pending_rows = [r for r in rows if r['Tipo'] == 'Revisar']
            enriched = {r['id']: r for r in enrich_transfers(pending_rows, emails)}
            updated = [enriched.get(r['id'], r) for r in rows]
            if updated != rows:
                st.session_state.records = updated
                st.session_state.month_dirty = True
                refresh_results()
                st.rerun()
            st.info('No se encontraron comentarios nuevos con coincidencia inequívoca.')
        except Exception:
            st.error('No se pudieron consultar los comentarios. Puedes seguir revisando los movimientos.')
    view = st.radio('Mostrar', ['Todos', 'Por revisar', 'Fijos', 'Variables', 'Abonos'], horizontal=True)
    query = st.text_input('Buscar comercio, destinatario o monto').strip().casefold()
    types = {'Por revisar': 'Revisar', 'Fijos': 'Fijo', 'Variables': 'Variable', 'Abonos': 'Ingreso'}
    selected = [r for r in rows if (view == 'Todos' or r['Tipo'] == types[view])
        and (not query or query in (r['Descripción'] + ' ' + str(r.get('_Original', '')) + ' ' + str(r['Monto'])).casefold())]
    if not selected:
        st.info('No hay movimientos que coincidan con estos filtros.')
    else:
        frame = pd.DataFrame(selected)
        frame['Revisión'] = ['Revisado por ti' if r.get('Revisado') else ('Por revisar' if r['Tipo'] == 'Revisar' else 'Clasificado automáticamente') for r in selected]
        st.dataframe(frame[['Fecha','Descripción','Monto','Tipo','Categoría','Responsable','Revisión']],
            hide_index=True, use_container_width=True,
            column_config={'Monto': st.column_config.NumberColumn('Monto CLP', format='$ %d')})
        row = st.selectbox('Abrir movimiento', selected, format_func=lambda r: f"{r['Fecha']} · {r['Descripción']} · $ {r['Monto']}")
        with st.expander('Detalle y corrección', expanded=True):
            st.caption('Fecha bancaria: ' + row['Fecha'])
            operation = re.search(r'\bel\s+(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})', row.get('_Original',''), re.I)
            if operation: st.caption('Fecha de operación en la glosa: ' + operation[1])
            rule = match_rule(row.get('_Original', row['Descripción']), active_rules(), row['Monto'])
            st.caption('Corrección manual conservada.' if row.get('Revisado') else ('Regla coincidente: ' + rule['match_text'] if rule else 'Sin regla coincidente; requiere revisión.'))
            with st.expander('Ver glosa original y origen'):
                st.text(row.get('_Original', row['Descripción']))
                st.caption(row.get('Fuente', ''))
            st.caption('Aplica los cambios antes de seleccionar otro movimiento. Esto no crea reglas futuras.')
            with st.form('movement_' + row['id'] + '_' + str(st.session_state.get('edit_revision', 0))):
                description = st.text_input('Descripción visible', value=row['Descripción'])
                note = st.text_input('Añadir nota a la descripción', placeholder='Ej.: Cabritas de fonda')
                kinds = ['Fijo','Variable','Ingreso','Ignorar','Revisar']
                kind = st.selectbox('Tipo de movimiento', kinds, index=kinds.index(row['Tipo']))
                category = st.text_input('Categoría', value=row['Categoría'])
                owners = ['Compartido','Personal','Por Revisar']
                owner = st.selectbox('Responsable', owners, index=owners.index(row['Responsable']))
                value = st.number_input('Monto CLP', value=int(row['Monto']) if row['Monto'] is not None else None, step=1)
                confirmed = st.checkbox('Corresponde al mes seleccionado', value=row.get('Período confirmado', True))
                if st.form_submit_button('Aplicar solo a este movimiento'):
                    if not category.strip() or not description.strip():
                        st.error('Completa descripción y categoría.')
                    elif category in FIXED and kind != 'Fijo':
                        st.error('Esta categoría pertenece a Gastos Fijos. Selecciona el tipo Fijo.')
                    else:
                        edited = dict(row, Descripción=description.strip() + (' — ' + note.strip() if note.strip() else ''),
                            Tipo=kind, Categoría=category.strip(), Responsable=owner, Monto=value)
                        edited['Período confirmado'] = confirmed
                        edited['Revisado'] = True
                        st.session_state.last_movement_edit = deepcopy(row)
                        updated = merge_edits(rows, [edited])
                        next(r for r in updated if r['id']==row['id'])['Revisado'] = True
                        st.session_state.records = updated
                        st.session_state.month_dirty = True
                        refresh_results()
                        st.session_state.edit_revision = st.session_state.get('edit_revision', 0) + 1
                        st.rerun()
            st.caption('Para repetir una clasificación, abre Reglas y revisa qué operaciones afectará antes de guardarla.')
    with st.expander('Exportar'):
        st.caption('Exportar no guarda los cambios del mes.')
        frame = pd.DataFrame(rows)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            frame.drop(columns=['_Original'], errors='ignore').to_excel(writer, index=False, sheet_name='Movimientos')
        st.download_button('Descargar Excel', output.getvalue(), file_name='Movimientos.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        if st.button('Exportar a Google Sheets'):
            from sheets_exporter import export_to_sheets
            values, _ = summarize(rows, st.session_state.get('beneficio_aplicado', 0))
            try:
                url = export_to_sheets(values, frame[frame.Tipo=='Variable'], frame[frame.Tipo=='Revisar'], frame[frame.Tipo=='Ingreso'])
                if url: st.link_button('Abrir archivo exportado', url)
                else: st.error('No se pudo completar la exportación.')
            except Exception:
                st.error('No se pudo exportar. Revisa la conexión de Google Sheets en la configuración.')
