import streamlit as st
import pandas as pd
from datetime import datetime

def export_to_sheets(resultados_dict, df_var, user_email):
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
        
        # Sheet 1: Gastos Fijos
        sheet1 = sh.sheet1
        sheet1.update_title("Gastos Fijos")
        
        rows1 = [["Fecha de Exportación", "Ítem Fijo", "Monto Detectado (CLP)"]]
        now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        for k, v in resultados_dict.items():
            if v > 0:
                rows1.append([now_str, k, v])
                
        sheet1.append_rows(rows1)
        sheet1.format('A1:C1', {'textFormat': {'bold': True}})
        
        # Sheet 2: Gastos Variables
        sheet2 = sh.add_worksheet(title="Gastos Variables", rows="100", cols="6")
        rows2 = [["Fecha", "Descripción", "Categoría", "Responsable", "Monto (CLP)"]]
        
        if df_var is not None and not df_var.empty:
            for _, row in df_var.iterrows():
                rows2.append([
                    str(row.get('Fecha', '')), 
                    str(row.get('Descripción', '')), 
                    str(row.get('Categoría', '')), 
                    str(row.get('Responsable', '')), 
                    int(row.get('Monto', 0))
                ])
                
        sheet2.append_rows(rows2)
        sheet2.format('A1:E1', {'textFormat': {'bold': True}})
        
        return sh.url
        
    except Exception as e:
        st.error(f"Error al exportar a Google Sheets: {e}")
        return False
