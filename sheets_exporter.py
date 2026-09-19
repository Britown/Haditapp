import streamlit as st
import pandas as pd
from datetime import datetime

def export_to_sheets(resultados_dict, df_identificados, df_no_identificados, df_ingresos):
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError:
        st.error("Falta instalar gspread y google-auth. Agrégalos a requirements.txt")
        return False

    try:
        if "gcp_service_account" not in st.secrets:
            st.error("No se encontraron credenciales en st.secrets.")
            return False
            
        credentials_dict = dict(st.secrets["gcp_service_account"])
        master_url = credentials_dict.get("master_sheet_url")
        
        if not master_url:
            st.error("No se encontró 'master_sheet_url' en los secretos.")
            return False
            
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        creds = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
        client = gspread.authorize(creds)
        
        # Open existing spreadsheet
        sh = client.open_by_url(master_url)
        
        suffix = f" {datetime.now().strftime('%d/%m %H:%M')}"
        
        def create_tab(name, cols=6):
            full_name = f"{name}{suffix}"
            try:
                return sh.add_worksheet(title=full_name, rows=100, cols=cols)
            except:
                # If there's a name collision
                return sh.add_worksheet(title=f"{full_name} {datetime.now().strftime('%S')}", rows=100, cols=cols)

        # Fijos
        sheet1 = create_tab("Fijos", cols=3)
        rows1 = [["Fecha de Exportación", "Ítem Fijo", "Monto Detectado (CLP)"]]
        now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        for k, v in resultados_dict.items():
            if v > 0:
                rows1.append([now_str, k, v])
        sheet1.append_rows(rows1)
        sheet1.format('A1:C1', {'textFormat': {'bold': True}})
        
        def _write_df_to_tab(tab_title, df):
            sheet = create_tab(tab_title, cols=6)
            rows = [["Fecha", "Descripción", "Categoría", "Responsable", "Monto (CLP)"]]
            if df is not None and not df.empty:
                for _, row in df.iterrows():
                    rows.append([
                        str(row.get('Fecha', '')), 
                        str(row.get('Descripción', '')), 
                        str(row.get('Categoría', '')), 
                        str(row.get('Responsable', '')), 
                        int(row.get('Monto', 0))
                    ])
            sheet.append_rows(rows)
            sheet.format('A1:E1', {'textFormat': {'bold': True}})

        _write_df_to_tab("Identificados", df_identificados)
        _write_df_to_tab("Por Revisar", df_no_identificados)
        _write_df_to_tab("Ingresos", df_ingresos)
        
        return sh.url
        
    except Exception as e:
        st.error(f"Error al exportar a Google Sheets: {e}")
        return False
