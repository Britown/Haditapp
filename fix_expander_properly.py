with open("app.py", "r") as f:
    content = f.read()

import re

# Find everything between `with col_left:` and `with col_right:`
start_idx = content.find("with col_left:")
end_idx = content.find("with col_right:")

new_col_left = """with col_left:
    st.markdown('''<div class="ui-card" style="padding-bottom: 24px;">
    <div class="card-header">VARIABLES CLAVE</div>
    <div class="card-title">Ajustes Dinámicos</div>
    <div class="card-subtitle" style="margin-bottom: 12px;">Variables macroeconómicas y tipo de cambio para indexación automática.</div>''''', unsafe_allow_html=True)
    
    with st.expander("⚙️ Mostrar Ajustes Dinámicos", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            valor_uf = st.number_input("Valor UF (CLP)", value=float(VALORES_BASE_MES.get("valor_uf", 37900.0)), step=10.0)
            dolar_val = st.number_input("Dólar Observado", value=VALORES_BASE_MES["valor_dolar"], step=10.0)
            pdf_password = st.text_input("Clave PDF Banco", type="password", help="Si tu banco protege la cartola, ingresa tu RUT o clave aquí.")
        with c2:
            manda_val = st.number_input("Mandarino (CLP)", value=VALORES_BASE_MES["mensualidad_mandarino"], step=1000)
            manda_mat_val = st.number_input("Mandarino Matrícula", value=220000, step=1000)
        with c3:
            beneficio_val = st.number_input("Beneficio Empresa", value=VALORES_BASE_MES["beneficio_empleador_por_hijo"], step=1000)
        
        st.markdown('<hr style="margin: 1rem 0; border-color: #e2e8f0;">', unsafe_allow_html=True)
        c4, c5 = st.columns(2)
        with c4:
            papa_pct = st.number_input("% Aporte Papá", value=63.77, step=0.1, format="%.2f")
        with c5:
            mama_pct = st.number_input("% Aporte Mamá", value=36.23, step=0.1, format="%.2f")
        csfj_val = VALORES_BASE_MES.get("uf_colegio", 13.5) * valor_uf

    st.markdown('<div style="margin-top: 24px;"></div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Arrastrar Archivos", "Pegar Texto"])
    with tab1:
        uploaded_files = st.file_uploader("Arrastra tu cartola bancaria", accept_multiple_files=True, label_visibility="collapsed")
    with tab2:
        pasted_text = st.text_area("Pega aquí la cartola", height=120, label_visibility="collapsed")
    st.button("Procesar Gastos Fijos (Cmd + Enter)", on_click=do_process)
    st.markdown('</div>', unsafe_allow_html=True)

"""

new_content = content[:start_idx] + new_col_left + content[end_idx:]
with open("app.py", "w") as f:
    f.write(new_content)
