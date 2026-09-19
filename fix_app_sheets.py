import re

with open("app.py", "r") as f:
    content = f.read()

# Add import
if "from sheets_exporter import export_to_sheets" not in content:
    content = content.replace(
        "from utils import format_clp, standardize_date, fetch_indicators",
        "from utils import format_clp, standardize_date, fetch_indicators\nfrom sheets_exporter import export_to_sheets"
    )

old_end = """
                </div>
            </section>
"""

new_end = """
                </div>
            </section>
            
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

content = content.replace(old_end.strip(), new_end.strip())

with open("app.py", "w") as f:
    f.write(content)
