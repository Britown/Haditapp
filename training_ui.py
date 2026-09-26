"""Persistent learning shared by both reconciliation screens."""
import streamlit as st
import pandas as pd
import database
from rules import seed_rules,validate_rule,suggest_pattern,rule_id
from workflow import effective_rules,apply_rules,split_school
from processor_v3 import summarize


def stored_rules():
    if 'saved_rules' not in st.session_state:
        try:configured='firebase' in st.secrets
        except Exception:configured=False
        if not configured:return [],0
        try:
            saved,revision=database.load_rulebook(database.get_db())
            st.session_state.saved_rules=saved;st.session_state.rule_revision=revision
        except Exception:
            st.error('No se pueden recuperar las reglas guardadas. Reintenta la conexión antes de procesar.')
            st.stop()
    return st.session_state.saved_rules,st.session_state.rule_revision


def selected_period():
    value=st.session_state.get('current_month_str','')
    return value.split()[-1]+'-12' if value else None


def active_rules():return effective_rules(seed_rules(),stored_rules()[0])


def refresh_results():
    rows=st.session_state.get('records',[])
    results,dates=summarize(rows,st.session_state.get('beneficio_aplicado',0))
    st.session_state.resultados_fijos=results;st.session_state.fechas_fijas=dates
    st.session_state.unmatched=[r for r in rows if r['Tipo']!='Fijo']
    st.session_state.pop('edited_variables',None)


def save_rule(rule):
    saved,revision=stored_rules();rule=validate_rule(rule)
    candidate=[r for r in saved if r.get('id',rule_id(r['match_text'],r.get('amount')))!=rule['id']]+[rule]
    revision=database.save_rulebook(database.get_db(),candidate,revision)
    st.session_state.saved_rules=candidate;st.session_state.rule_revision=revision
    if 'records' in st.session_state:
        st.session_state.records=apply_rules(st.session_state.records,effective_rules(seed_rules(),candidate),period=selected_period())
        refresh_results()


def render():
    st.header('Entrenar gastos fijos y variables')
    saved,revision=stored_rules()
    rows=st.session_state.get('records',[])
    row=st.selectbox('Movimiento de ejemplo',rows,format_func=lambda r:f"{r['Fecha']} · {r['Descripción']} · $ {r['Monto']}") if rows else None
    with st.form('training_'+(row['id'] if row else 'manual')):
        pattern=st.text_input('Comercio o destinatario que se repite',value=suggest_pattern(row['_Original']) if row else '')
        kind=st.selectbox('Tipo',['Fijo','Variable','Ingreso','Ignorar'])
        category=st.text_input('Concepto o categoría',value=row['Categoría'] if row else '')
        owner=st.selectbox('Responsable',['Compartido','Personal'])
        exact=st.checkbox('Usar esta regla solo para este monto',value=bool(row and 'CSFJ' in row['Categoría']),help='Útil cuando el colegio no distingue conceptos en la glosa. Otros montos quedarán para revisión.')
        value=st.number_input('Monto de la regla (CLP)',min_value=0,value=int(abs(row['Monto'] or 0)) if row else 0)
        st.caption('El aprendizaje se guarda en Firebase, se puede editar y se reutiliza el próximo mes. Para desglosar un pago del colegio usa la sección inferior.')
        if st.form_submit_button('Guardar regla y aplicar'):
            try:
                save_rule(dict(match_text=pattern,kind=kind,category=category,owner=owner,priority=100,enabled=True,amount=value if exact else None))
                st.success('Regla guardada y aplicada. Revisa el resultado en Gastos Fijos o Variables.')
            except Exception as e:st.error(str(e) if isinstance(e,ValueError) else 'No se pudo guardar la regla. Comprueba Firebase; no se aplicó el cambio.')
    if row and 'CSFJ' in row['Categoría'] and not row.get('parent_id'):
        with st.expander('Desglosar pago del colegio',expanded=True):
            with st.form('split_'+row['id']):
                from rules import FIXED
                values={cat:st.number_input(cat,min_value=0,value=0,step=1) for cat in FIXED if cat.startswith('CSFJ')}
                if st.form_submit_button('Aplicar desglose'):
                    try:
                        st.session_state.records=split_school(rows,row['id'],values);refresh_results();st.success('Desglose aplicado. Guarda la conciliación para conservarlo.')
                    except ValueError as e:st.error(str(e))
    st.subheader('Reglas guardadas')
    if saved:
        columns=['match_text','kind','category','owner','amount','priority','enabled']
        with st.form('edit_rules_'+str(revision)):
            edited=st.data_editor(pd.DataFrame(saved).reindex(columns=columns),hide_index=True,use_container_width=True)
            if st.form_submit_button('Guardar cambios de reglas'):
                try:
                    import json
                    candidate=[validate_rule(r) for r in json.loads(edited.to_json(orient='records'))]
                    revision=database.save_rulebook(database.get_db(),candidate,revision)
                    st.session_state.saved_rules=candidate;st.session_state.rule_revision=revision
                    if rows:st.session_state.records=apply_rules(rows,effective_rules(seed_rules(),candidate),period=selected_period());refresh_results()
                    st.rerun()
                except Exception as e:st.error(str(e) if isinstance(e,ValueError) else 'No se guardaron los cambios. Revisa la conexión.')
    else:st.info('Aún no hay reglas nuevas guardadas en Firebase.')
    if st.button('Recargar reglas'):
        st.session_state.pop('saved_rules',None);st.rerun()
