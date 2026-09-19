import re

with open("sheets_exporter.py", "r") as f:
    sheets_content = f.read()

sheets_content = sheets_content.replace(
    "def export_to_sheets(resultados_dict):",
    "def export_to_sheets(resultados_dict, sheet_url):"
)

old_url_logic = """
        # We need the Google Sheet ID or URL from the user. 
        # For now, let's assume it's in the secrets or we can ask the user in the UI.
        sheet_url = st.secrets.get("google_sheet_url", "")
        if not sheet_url:
            st.error("Falta la URL de la planilla (google_sheet_url) en los secretos.")
            return False
"""

new_url_logic = """
        if not sheet_url:
            st.error("Por favor, ingresa una URL válida de Google Sheets.")
            return False
"""
sheets_content = sheets_content.replace(old_url_logic.strip(), new_url_logic.strip())

with open("sheets_exporter.py", "w") as f:
    f.write(sheets_content)


with open("app.py", "r") as f:
    app_content = f.read()

old_app_logic = """
            # --- Google Sheets Export ---
            st.markdown("<br>", unsafe_allow_html=True)
            if "gcp_service_account" in st.secrets and "google_sheet_url" in st.secrets:
                if st.button("Exportar a Google Sheets", type="primary", use_container_width=True):
                    with st.spinner("Guardando en la nube..."):
                        if export_to_sheets(resultados):
                            st.success("¡Exportado correctamente a Google Sheets!")
            else:
                with st.expander("Integrar con Google Sheets"):
                    st.info("Falta configurar las credenciales de Google. Agrega `gcp_service_account` y `google_sheet_url` a tus secretos de Streamlit (o localmente en `.streamlit/secrets.toml`).")
"""

new_app_logic = """
            # --- Google Sheets Export ---
            st.markdown("<br>", unsafe_allow_html=True)
            if "gcp_service_account" in st.secrets:
                st.markdown("<h4 style='font-size: 14px; font-weight: 600; color: #1D1D1F; margin-bottom: 8px;'>Exportar resultados</h4>", unsafe_allow_html=True)
                sheet_input_url = st.text_input("Pega el link de la planilla de Google Sheets aquí:", placeholder="https://docs.google.com/spreadsheets/d/...", label_visibility="collapsed")
                
                if st.button("Exportar a esta planilla", type="primary", use_container_width=True, disabled=not sheet_input_url.strip()):
                    with st.spinner("Conectando con Google..."):
                        if export_to_sheets(resultados, sheet_input_url.strip()):
                            st.success("¡Gastos guardados con éxito en la planilla!")
                            
                st.markdown("<p style='font-size: 11px; color: #86868B;'>* Recuerda darle permisos de Editor al correo del bot en la planilla antes de exportar.</p>", unsafe_allow_html=True)
            else:
                with st.expander("Integrar con Google Sheets"):
                    st.info("Falta configurar las credenciales de Google. Agrega `gcp_service_account` a tus secretos de Streamlit.")
"""

app_content = app_content.replace(old_app_logic.strip(), new_app_logic.strip())

with open("app.py", "w") as f:
    f.write(app_content)

