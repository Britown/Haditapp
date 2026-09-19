import re

with open("app.py", "r") as f:
    content = f.read()

# Store resultados in session_state
content = content.replace(
    "st.toast('✨ ¡Cálculo mágico completado con éxito!', icon='🪄')",
    "st.toast('✨ ¡Cálculo mágico completado con éxito!', icon='🪄')\n                st.session_state.resultados_fijos = resultados"
)

# Extract the export block exactly
export_block = """
                # --- Google Sheets Export ---
                st.markdown("<br>", unsafe_allow_html=True)
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
                    with st.expander("Integrar con Google Sheets"):
                        st.info("Falta configurar las credenciales de Google. Agrega `gcp_service_account` a tus secretos de Streamlit.")
"""
content = content.replace(export_block, "\n")


new_export_block = """

    # Botón de exportación al final
    if st.session_state.get("unmatched") is not None and st.session_state.get("resultados_fijos") is not None:
        import pandas as pd
        
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
                sheet_input_email = st.text_input("Ingresa tu correo de Gmail para enviarte el archivo:", placeholder="tu.correo@gmail.com")
                
                if st.button("Crear Excel en Google Drive", type="primary", use_container_width=True, disabled=not sheet_input_email.strip()):
                    with st.spinner("Creando archivo en la nube..."):
                        new_url = export_to_sheets(st.session_state.resultados_fijos, final_df, sheet_input_email.strip())
                        if new_url:
                            st.success(f"¡Listo! Archivo creado exitosamente.")
                            st.markdown(f"**[Haz clic aquí para abrir tu nueva planilla]({new_url})**", unsafe_allow_html=True)
                            
                st.markdown("<p style='font-size: 11px; color: #86868B; text-align: center;'>Se creará un archivo nuevo automáticamente con 2 pestañas (Fijos y Variables) y se compartirá con tu Drive.</p>", unsafe_allow_html=True)
            else:
                st.info("Falta configurar las credenciales de Google. Agrega `gcp_service_account` a tus secretos de Streamlit.")
"""

# We need to append `new_export_block` at the very bottom of the script.
# The script ends around line 550, which is the end of `with st.expander("💳 Gastos Variables...", expanded=True):` block
# Let's just append it.

content += new_export_block

with open("app.py", "w") as f:
    f.write(content)
