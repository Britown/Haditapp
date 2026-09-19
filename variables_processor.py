import pandas as pd
from utils import standardize_date
import json
import re
import streamlit as st

def load_rules():
    try:
        df = pd.read_csv("reglas_variables.csv")
        return df.to_dict('records')
    except:
        return []

RULES = load_rules()

def clean_fallback(desc):
    # Remove prefix dates like "03/08 "
    desc = re.sub(r'^\d{2}/\d{2}\s+', '', desc)
    desc = re.sub(r'^(Cargo por Compra en|Cargo por transferencia a Rut [\d\.\-kK]+|Abono por transferencia de|Transferencia de)\s+', '', desc, flags=re.IGNORECASE)
    desc = re.sub(r'(?i)\s+(el|El|desde)\s+\d{2}/\d{2}/\d{4}.*$', '', desc)
    desc = re.sub(r'(?i)\s+(el|El)\s+[\d\.\,]+.*$', '', desc) # removes " El 3.490,00..."
    desc = re.sub(r'(?i)\s+a las\s+\d{2}:\d{2}.*$', '', desc)
    desc = re.sub(r'(?i),\s*Monto\s*[\d\.\,]+$', '', desc)
    desc = re.sub(r'(?i)\s+el\s+\d{4}-\d{2}-\d{2}.*$', '', desc)
    
    desc = re.sub(r'^(SANTIAGO|LAS CONDES|PROVIDENCIA)\s+\d{2}/\d{2}/\d{2}\s+\d{4}\s+\d+\s+', '', desc, flags=re.IGNORECASE)
    desc = re.sub(r'\s*\$?\s*[\d\.\,]+\s*$', '', desc)
    desc = re.sub(r'\s+\d{2}/\d{2}\s+\$?\s*[\d\.\,]+.*$', '', desc)
    desc = re.sub(r'\s*\$\s*[\d\.\,]+\s*\$\s*[\d\.\,]+.*$', '', desc)
    desc = re.sub(r'(?i)\s+TASA\s+INT\.?\s*[\d\.\,]+%.*$', '', desc)
    
    return desc.strip().title()

@st.cache_data
def _categorize_with_ai_cached(descriptions_tuple):
    descriptions = list(descriptions_tuple)
    if not descriptions:
        return {}
    
    try:
        api_key = st.secrets.get("firebase", {}).get("gemini_api_key")
        if not api_key:
            return {}
            
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        Actúa como un experto contable chileno familiar. 
        Tienes una lista de descripciones de cobros bancarios brutos. Necesito que hagas 3 cosas para cada uno:
        
        1. Limpiar el nombre ("clean_desc"): Remueve fechas, montos, la palabra "Monto", y frases basura como "Cargo por Compra en", "Transferencia a Rut", etc. Deja solo el nombre real del comercio o persona en formato Título (Title Case).
        2. Asignar Categoría ("cat"): Debe ser EXACTAMENTE UNA de estas: ["Supermercado", "Farmacia", "Gustitos", "Delivery", "Salud", "Combustible", "Suscripciones", "Entretenimiento", "Seguros", "Babysit", "Librería", "Minimarket", "Pago cuota casa", "Pago deuda Omita", "Gastos Bancarios", "Pago Tarjeta", "Mercadería", "Compras hogar", "Restaurant-café", "Ingresos", "Mercado Pago", "Por Revisar"]
        3. Asignar Responsable ("own"): Debe ser EXACTAMENTE UNA de estas: ["Compartido", "Personal", "Por Revisar"]
        
        Reglas:
        - Jumbo, Lider, Santa Isabel, Unimarc -> Supermercado / Compartido
        - Cruz Verde, Salcobrand, Clínicas, Médicos, Farma -> Farmacia o Salud / Compartido
        - Copec, Shell, Petrobras, Autopistas -> Combustible / Personal
        - Uber, Cabify -> Transporte (Gustitos) / Personal
        - Restaurantes, Cafés, Heladerías, "Pedro Fon", "Bakery", "Mc Donalds" -> Restaurant-café / Compartido
        - Rappi, PedidosYa, Spid -> Delivery / Compartido
        - Spotify, Netflix, Zapping, Prime -> Suscripciones / Personal
        - Transferencias a personas -> Por Revisar / Por Revisar (A menos que sepas qué es)
        
        Devuelve un JSON válido donde las llaves sean las descripciones EXACTAS solicitadas y el valor sea el objeto con 'clean_desc', 'cat' y 'own'.
        Ejemplo:
        {{
            "Cargo por Compra en JUMBO PEÑALOLEN El 02/08/2026 Monto 1500": {{"clean_desc": "Jumbo Peñalolén", "cat": "Supermercado", "own": "Compartido"}},
            "Cargo por transferencia a Rut 10.897.701-9 Mercado Pago, el 03/08": {{"clean_desc": "Mercado Pago", "cat": "Mercado Pago", "own": "Por Revisar"}}
        }}
        
        Descripciones a procesar:
        {json.dumps(descriptions)}
        """
        
        # Intentar con 3.5, si falla por demanda, intentar con 2.5
        model_names = ['gemini-3.5-flash', 'gemini-3.6-flash', 'gemini-3.7-flash', 'gemini-3.8-flash']
        last_error = None
        for m_name in model_names:
            try:
                response = client.models.generate_content(
                    model=m_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                    ),
                )
                return json.loads(response.text)
            except Exception as e:
                last_error = e
                if '503' not in str(e) and '429' not in str(e):
                    break # if it's not a demand/quota issue, stop trying
        
        st.error(f"Error de AI: {last_error}")
        return {}
    except Exception as e:
        st.error(f"Error de AI: {e}")
        return {}

def categorize_with_ai(descriptions):
    return _categorize_with_ai_cached(tuple(descriptions))

def classify_variable(glosa, monto):
    glosa_upper = glosa.upper()
    for rule in load_rules():
        match = str(rule.get('match_text', '')).upper()
        if match and match in glosa_upper:
            clean_name = rule.get('clean_name')
            if pd.isna(clean_name): clean_name = None
            
            if match in ["COPEC ASISTIDO", "SHELL", "ARAMCO"]:
                if monto > 40000:
                    return "Combustible", "Personal", clean_name
                elif monto < 10000:
                    return "Combustible", "Personal", clean_name
                else:
                    return "Combustible", "Compartido", clean_name
            return rule.get('category', 'Sin Categorizar'), rule.get('owner', 'Confirmar'), clean_name
            
    
    if "SUELDO" in glosa_upper or "REMUNERACION" in glosa_upper or "REEMBOLSO" in glosa_upper or "ABONO" in glosa_upper:
        return "Ingresos", "Personal", None
        
    if "HERNAN BRITO VIDAL" in glosa_upper:
        if monto >= 900000:
            return "Pago cuota casa", "Compartido", "Pago a Hernan Alberto"
        else:
            return "Por Revisar", "Por Revisar", "Pago a Hernan Alberto"
            
    if "15.935.026-6" in glosa_upper or "VANESSA CAROLINA" in glosa_upper:
        if monto == 230000:
            return "Pago deuda Omita", "Personal", "Transf. a Vane"
        else:
            return "Por Revisar", "Por Revisar", "Transf. a Vane"
        
    return "Por Revisar", "Por Revisar", None

def process_unmatched_to_df(unmatched_list):
    processed = []
    
    # Send ALL unmatched to AI so we get a clean description for everything
    unique_descs = sorted(list(set([item["Descripción"] for item in unmatched_list])))
    ai_results = categorize_with_ai(unique_descs)
    
    for item in unmatched_list:
        raw_desc = item["Descripción"]
        cat_rule, owner_rule, clean_name_rule = classify_variable(raw_desc, item["Monto"])
        
        if cat_rule == "Gastos fijos":
            continue
            
        res = ai_results.get(raw_desc, {})
        
        clean_desc = res.get("clean_desc", clean_fallback(raw_desc))
        if clean_name_rule:
            clean_desc = clean_name_rule
        
        # Prefer rule category if it's not "Por Revisar"
        if cat_rule not in ["Por Revisar", "Sin Categorizar"]:
            cat = cat_rule
            owner = owner_rule
        else:
            cat = res.get("cat", "Por Revisar")
            owner = res.get("own", "Por Revisar")
            
        processed.append({
            "Fecha": standardize_date(item["Fecha"]),
            "Descripción": clean_desc,
            "Categoría": cat,
            "Responsable": owner,
            "Monto": item["Monto"],
            "_Original": raw_desc
        })
        
    return pd.DataFrame(processed)
