with open("app.py", "r") as f:
    content = f.read()

old_app_logic = """
                if "gcp_service_account" in st.secrets:
                    st.markdown("<h4 style='font-size: 14px; font-weight: 600; color: #1D1D1F; margin-bottom: 8px;'>Exportar resultados</h4>", unsafe_allow_html=True)
                    sheet_input_url = st.text_input("Pega el link de la planilla de Google Sheets aquí:", placeholder="https://docs.google.com/spreadsheets/d/...", label_visibility="collapsed")
                    
                    if st.button("Exportar a esta planilla", type="primary", use_container_width=True, disabled=not sheet_input_url.strip()):
                        with st.spinner("Conectando con Google..."):
                            if export_to_sheets(resultados, sheet_input_url.strip()):
                                st.success("¡Gastos guardados con éxito en la planilla!")
                                
                    st.markdown("<p style='font-size: 11px; color: #86868B;'>* Recuerda darle permisos de Editor al correo del bot en la planilla antes de exportar.</p>", unsafe_allow_html=True)
                else:
"""

new_app_logic = """
                if "gcp_service_account" in st.secrets:
                    st.markdown("<h4 style='font-size: 14px; font-weight: 600; color: #1D1D1F; margin-bottom: 8px;'>Exportar resultados</h4>", unsafe_allow_html=True)
                    sheet_input_email = st.text_input("Ingresa tu correo de Gmail para enviarte el archivo:", placeholder="tu.correo@gmail.com", label_visibility="collapsed")
                    
                    if st.button("Crear Excel en Google Drive", type="primary", use_container_width=True, disabled=not sheet_input_email.strip()):
                        with st.spinner("Creando archivo en la nube..."):
                            new_url = export_to_sheets(resultados, sheet_input_email.strip())
                            if new_url:
                                st.success(f"¡Listo! Archivo creado exitosamente.")
                                st.markdown(f"**[Haz clic aquí para abrir tu nueva planilla]({new_url})**", unsafe_allow_html=True)
                                
                    st.markdown("<p style='font-size: 11px; color: #86868B;'>* Se creará un archivo nuevo automáticamente y se compartirá con tu Drive.</p>", unsafe_allow_html=True)
                else:
"""

content = content.replace(old_app_logic.strip(), new_app_logic.strip())

with open("app.py", "w") as f:
    f.write(content)
