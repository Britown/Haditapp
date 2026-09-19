with open("app.py", "r") as f:
    lines = f.readlines()

# 1. Identify the export block at the bottom
start_idx = -1
for i, l in enumerate(lines):
    if "# Botón de exportación al final" in l:
        start_idx = i
        break

if start_idx != -1:
    export_block = "".join(lines[start_idx:])
    lines = lines[:start_idx] # Remove from bottom
else:
    print("Could not find export block")
    exit(1)

# 2. Indent the export block so it fits inside the "Gastos Variables" page
# We only need the code inside the block, not the `if st.session_state.get...` check because we are already inside `if 'unmatched' in st.session_state and st.session_state.unmatched:`
inner_block = """
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

# 3. Find the local download button
insert_idx = -1
for i, l in enumerate(lines):
    if 'mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"' in l:
        insert_idx = i + 2 # After the closing parenthesis of st.download_button
        break

if insert_idx != -1:
    lines.insert(insert_idx, inner_block + "\n")
else:
    print("Could not find download button")
    exit(1)

with open("app.py", "w") as f:
    f.writelines(lines)

