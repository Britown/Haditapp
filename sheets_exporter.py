import streamlit as st
import pandas as pd
from datetime import datetime

def export_to_sheets(resultados_dict, user_email):
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError:
        st.error("Falta instalar gspread y google-auth. Agrégalos a requirements.txt")
        return False

    try:
        # Load credentials from Streamlit secrets
        if "gcp_service_account" not in st.secrets:
            st.error("No se encontraron las credenciales de Google (gcp_service_account) en los secretos de Streamlit.")
            return False
            
        credentials_dict = dict(st.secrets["gcp_service_account"])
        
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        creds = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
        client = gspread.authorize(creds)
        
        if not sheet_url or "@" not in sheet_url:
            st.error("Por favor, ingresa un correo electrónico válido.")
            return False
            
        user_email = sheet_url.strip()
        
        # Create a new spreadsheet
        title = f"Haditapp - Gastos {datetime.now().strftime('%d %b %Y %H:%M')}"
        sh = client.create(title)
        
        # Share it with the user so they can see it in their Google Drive
        sh.share(user_email, perm_type='user', role='writer')
        
        sheet = sh.sheet1
        
        # Prepare data headers and rows
        rows = [["Fecha de Exportación", "Ítem de Gasto", "Monto Detectado (CLP)"]]
        now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        for k, v in resultados_dict.items():
            if v > 0:
                rows.append([now_str, k, v])
                
        # Append rows
        sheet.append_rows(rows)
        
        # Format header
        sheet.format('A1:C1', {'textFormat': {'bold': True}})
        
        return sh.url
        
    except Exception as e:
        st.error(f"Error al exportar a Google Sheets: {e}")
        return False
