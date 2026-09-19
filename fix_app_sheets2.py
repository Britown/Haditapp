with open("app.py", "r") as f:
    content = f.read()

old_code = """
                st.toast('✨ ¡Cálculo mágico completado con éxito!', icon='🪄')
"""

new_code = """
                st.toast('✨ ¡Cálculo mágico completado con éxito!', icon='🪄')
                
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

content = content.replace(old_code, new_code)

with open("app.py", "w") as f:
    f.write(content)
