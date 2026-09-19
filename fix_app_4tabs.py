import re

with open("app.py", "r") as f:
    content = f.read()

old_app_logic = """
        # Combine edited dataframes
        try:
            final_df = pd.concat([edited_identificados, edited_no_identificados, edited_ingresos], ignore_index=True)
        except:
            final_df = None
            
        st.markdown("<br><hr><br>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #1D1D1F;'>Exportar a Excel</h3>", unsafe_allow_html=True)
        
        col_space1, col_exp, col_space2 = st.columns([1, 2, 1])
        with col_exp:
            if "gcp_service_account" in st.secrets:
                sheet_input_email = st.text_input("Ingresa tu correo de Gmail para enviarte el archivo:", value="hbrito@gmail.com", placeholder="tu.correo@gmail.com")
                
                if st.button("Crear Excel en Google Drive", type="primary", use_container_width=True, disabled=not sheet_input_email.strip()):
                    with st.spinner("Creando archivo en la nube..."):
                        new_url = export_to_sheets(st.session_state.resultados_fijos, final_df, sheet_input_email.strip())
                        if new_url:
                            st.success(f"¡Listo! Archivo creado exitosamente.")
                            st.markdown(f"**[Haz clic aquí para abrir tu nueva planilla]({new_url})**", unsafe_allow_html=True)
                            
                st.markdown("<p style='font-size: 11px; color: #86868B; text-align: center;'>Se creará un archivo nuevo automáticamente con 2 pestañas (Fijos y Variables) y se compartirá con tu Drive.</p>", unsafe_allow_html=True)
"""

new_app_logic = """
        st.markdown("<br><hr><br>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #1D1D1F;'>Exportar a Excel</h3>", unsafe_allow_html=True)
        
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
"""

content = content.replace(old_app_logic.strip(), new_app_logic.strip())

with open("app.py", "w") as f:
    f.write(content)
