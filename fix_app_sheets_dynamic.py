import re

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
