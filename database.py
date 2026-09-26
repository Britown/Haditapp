import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import datetime

@st.cache_resource
def get_db():
    if not firebase_admin._apps:
        try:
            cert_dict = dict(st.secrets["firebase"])
            cred = credentials.Certificate(cert_dict)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Error conectando a Firebase: {e}")
            return None
    return firestore.client()

def save_month_data(db, month_year, total, papa, mama, papa_pct, mama_pct, resultados, fechas):
    if not db:
        return False
        
    doc_ref = db.collection("historial_gastos_fijos").document(month_year)
    
    # We use set with merge=True so we can overwrite an existing month if re-processed
    data = {
        "month_year": month_year,
        "total_neto": total,
        "aporte_papa": papa,
        "aporte_mama": mama,
        "pct_papa": papa_pct,
        "pct_mama": mama_pct,
        "desglose": resultados,
        "fechas_detectadas": fechas,
        "updated_at": firestore.SERVER_TIMESTAMP
    }
    
    try:
        doc_ref.set(data, merge=True)
        return True
    except Exception as e:
        st.error(f"Error guardando datos: {e}")
        return False

def save_gastos_variables(db, month_year, df_vars):
    if not db:
        return False
        
    doc_ref = db.collection("historial_gastos_variables").document(month_year)
    
    # Convert DataFrame to list of dicts
    import json
    # Use to_json to handle datatypes correctly
    gastos_json = json.loads(df_vars.to_json(orient='records'))
    
    # Separa gastos de ingresos
    df_gastos = df_vars[df_vars["Categoría"] != "Ingresos"]
    df_ingresos = df_vars[df_vars["Categoría"] == "Ingresos"]
    
    total_compartido = float(df_gastos[df_gastos["Responsable"] == "Compartido"]["Monto"].sum())
    total_personal = float(df_gastos[df_gastos["Responsable"] == "Personal"]["Monto"].sum())
    total_ingresos = float(df_ingresos["Monto"].sum())
    
    data = {
        "month_year": month_year,
        "gastos": gastos_json,
        "total_compartido": total_compartido,
        "total_personal": total_personal,
        "total_ingresos": total_ingresos,
        "updated_at": firestore.SERVER_TIMESTAMP
    }
    
    try:
        doc_ref.set(data, merge=True)
        return True
    except Exception as e:
        import streamlit as st
        st.error(f"Error guardando gastos variables: {e}")
        return False

def get_all_historial(db):
    if not db:
        return []
    try:
        docs = db.collection("historial_gastos_fijos").order_by("updated_at", direction=firestore.Query.DESCENDING).get()
        return docs
    except Exception as e:
        import streamlit as st
        st.error(f"Error obteniendo historial: {e}")
        return []


def load_rulebook(db):
    """None is a connection failure, never an empty set of learned rules."""
    if db is None:
        raise RuntimeError('Configura Firebase para guardar y recuperar el entrenamiento.')
    snapshot = db.collection('haditapp_config').document('rules').get()
    data = snapshot.to_dict() if snapshot.exists else {}
    return data.get('rules', []), data.get('revision', 0)


def save_rulebook(db, rules, expected_revision, variables=None):
    from rules import validate_rule
    validated = [validate_rule(r) for r in rules]
    if len({r['id'] for r in validated}) != len(validated):
        raise ValueError('Hay reglas duplicadas para el mismo patrón. Edita la existente.')
    ref = db.collection('haditapp_config').document('rules')
    transaction = db.transaction()

    @firestore.transactional
    def update(tx):
        snap = ref.get(transaction=tx)
        current = snap.to_dict() if snap.exists else {}
        revision = current.get('revision', 0)
        if revision != expected_revision:
            raise ValueError('Las reglas cambiaron en otra sesión. Recarga antes de guardar.')
        tx.set(ref, {'rules':validated,'revision':revision+1,'updated_at':firestore.SERVER_TIMESTAMP})
        if variables is not None:
            month, frame = variables
            import json
            expenses=frame[~frame['Categoría'].isin(['Ingresos','Ignorar'])]
            tx.set(db.collection('historial_gastos_variables').document(month), {
                'month_year':month, 'gastos':json.loads(frame.to_json(orient='records')),
                'total_compartido':float(expenses.loc[expenses['Responsable']=='Compartido','Monto'].sum()),
                'total_personal':float(expenses.loc[expenses['Responsable']=='Personal','Monto'].sum()),
                'total_ingresos':float(frame.loc[frame['Categoría']=='Ingresos','Monto'].sum()),
                'updated_at':firestore.SERVER_TIMESTAMP})
        return revision+1
    return update(transaction)


def save_reconciliation(db, state):
    """Atomically persist the editable ledger and legacy history projections."""
    import json
    from processor_v3 import summarize
    from money import clp
    from config import FACTORES_DIVISION
    if db is None:
        raise RuntimeError('No hay conexión con Firebase. No se ha guardado.')
    safe = json.loads(json.dumps(state, allow_nan=False))
    rows = safe['records']
    values, dates = summarize(rows,safe['beneficio'])
    total=sum(values.values());papa=clp(total*FACTORES_DIVISION['PAPA']);mama=total-papa
    batch = db.batch()
    key=safe['period']
    batch.set(db.collection('conciliaciones').document(key), {**safe,'updated_at':firestore.SERVER_TIMESTAMP})
    batch.set(db.collection('historial_gastos_fijos').document(key), {
        'month_year':key,'total_neto':total,'aporte_papa':papa,'aporte_mama':mama,
        'pct_papa':FACTORES_DIVISION['PAPA']*100,'pct_mama':FACTORES_DIVISION['MAMA']*100,
        'desglose':values,'fechas_detectadas':dates,'updated_at':firestore.SERVER_TIMESTAMP})
    variables=[r for r in rows if r['Tipo'] in ['Variable','Ingreso','Revisar']]
    batch.set(db.collection('historial_gastos_variables').document(key),{
        'month_year':key,'gastos':variables,
        'total_compartido':sum(r.get('Monto') or 0 for r in variables if r['Tipo']=='Variable' and r['Responsable']=='Compartido'),
        'total_personal':sum(r.get('Monto') or 0 for r in variables if r['Tipo']=='Variable' and r['Responsable']=='Personal'),
        'total_ingresos':sum(r.get('Monto') or 0 for r in variables if r['Tipo']=='Ingreso'),
        'updated_at':firestore.SERVER_TIMESTAMP})
    batch.commit()
    return True


def list_reconciliations(db):
    if db is None: raise RuntimeError('No hay conexión con Firebase.')
    return [dict(doc.to_dict(),id=doc.id) for doc in db.collection('conciliaciones').order_by('updated_at',direction=firestore.Query.DESCENDING).stream()]
