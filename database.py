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
