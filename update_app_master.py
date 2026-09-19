import re

with open("app.py", "r") as f:
    content = f.read()

old_block = """
        st.markdown("<br><hr><br>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #1D1D1F;'>Exportar a Google Sheets</h3>", unsafe_allow_html=True)
        
        col_space1, col_exp, col_space2 = st.columns([1, 2, 1])
        with col_exp:
            if "gcp_service_account" in st.secrets:
                sheet_input_email = st.text_input("Ingresa tu correo de Gmail para enviarte el archivo:", value="hbrito@gmail.com", placeholder="tu.correo@gmail.com")
                
                if st.button("Crear Excel en Google Drive", type="primary", use_container_width=True, disabled=not sheet_input_email.strip()):
                    with st.spinner("Creando archivo en la nube... (esto puede tomar unos 10 segundos)"):
                        new_url = export_to_sheets(
                            st.session_state.resultados_fijos, 
                            edited_identificados, 
                            edited_no_identificados, 
                            edited_ingresos, 
                            sheet_input_email.strip()
                        )
                        if new_url:
                            st.success(f"¡Listo! Archivo creado exitosamente.")
                            st.markdown(f"**[Haz clic aquí para abrir tu nueva planilla]({new_url})**", unsafe_allow_html=True)
                            
                st.markdown("<p style='font-size: 11px; color: #86868B; text-align: center;'>Se creará un archivo nuevo automáticamente con 4 pestañas y se compartirá con tu Drive.</p>", unsafe_allow_html=True)
            else:
                st.info("Falta configurar las credenciales de Google. Agrega `gcp_service_account` a tus secretos de Streamlit.")
"""

new_block = """
        st.markdown("<br><hr><br>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #1D1D1F;'>Exportar a Archivo Maestro</h3>", unsafe_allow_html=True)
        
        col_space1, col_exp, col_space2 = st.columns([1, 2, 1])
        with col_exp:
            gcp_secrets = st.secrets.get("gcp_service_account", {})
            if "private_key" in gcp_secrets:
                if "master_sheet_url" not in gcp_secrets:
                    st.warning("Falta agregar `master_sheet_url` en tus secretos de Streamlit (debajo de private_key).")
                else:
                    if st.button("Subir mes a Google Sheets", type="primary", use_container_width=True):
                        with st.spinner("Conectando con tu archivo maestro... (esto puede tomar unos segundos)"):
                            new_url = export_to_sheets(
                                st.session_state.resultados_fijos, 
                                edited_identificados, 
                                edited_no_identificados, 
                                edited_ingresos
                            )
                            if new_url:
                                st.success(f"¡Listo! Pestañas del mes agregadas exitosamente.")
                                st.markdown(f"**[Haz clic aquí para ir a tu Archivo Maestro]({new_url})**", unsafe_allow_html=True)
                                
                    st.markdown("<p style='font-size: 11px; color: #86868B; text-align: center;'>Se agregarán 4 pestañas nuevas a tu archivo maestro existente.</p>", unsafe_allow_html=True)
            else:
                st.info("Falta configurar las credenciales de Google. Agrega `gcp_service_account` a tus secretos de Streamlit.")
"""

content = content.replace(old_block.strip(), new_block.strip())

with open("app.py", "w") as f:
    f.write(content)
