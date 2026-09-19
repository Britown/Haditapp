import streamlit as st
import pandas as pd
from datetime import datetime

def export_to_sheets(resultados_dict, sheet_url):
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
        
        if not sheet_url:
            st.error("Por favor, ingresa una URL válida de Google Sheets.")
            return False
            
        sheet = client.open_by_url(sheet_url).sheet1
        
        # Prepare data: Date, Name, Amount
        now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        rows = []
        for k, v in resultados_dict.items():
            if v > 0:
                rows.append([now_str, k, v])
                
        # Append rows
        sheet.append_rows(rows)
        return True
        
    except Exception as e:
        st.error(f"Error al exportar a Google Sheets: {e}")
        return False
