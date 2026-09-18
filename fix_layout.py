with open("app.py", "r") as f:
    content = f.read()

# 1. Remove the <br>
content = content.replace('        st.markdown("<br>", unsafe_allow_html=True)\n', '')

# We need to extract the dos sections.
# Section 1: Ajustes Dinámicos
sect1_start = content.find("        st.markdown('<section class=\"bg-surface-container-lowest p-space-xl rounded-lg shadow-sm flex flex-col gap-space-lg\" style=\"background-color: rgb(255, 255, 255); border: 1px solid rgb(226, 232, 240); box-shadow: rgba(15, 23, 42, 0.06) 0px 4px 16px -2px;\">', unsafe_allow_html=True)\n        st.markdown(r\"\"\"<div class=\"flex flex-col\">\n    <span class=\"font-label-sm uppercase tracking-wider text-on-surface-variant\">Variables Clave</span>")
sect1_end = content.find("        st.markdown('</section><br>', unsafe_allow_html=True)\n") + len("        st.markdown('</section><br>', unsafe_allow_html=True)\n")

# Section 2: Ingesta de Cartolas
sect2_start = content.find("        st.markdown('<section class=\"bg-surface-container-lowest p-space-xl rounded-lg shadow-sm flex flex-col gap-space-lg\" style=\"background-color: rgb(255, 255, 255); border: 1px solid rgb(226, 232, 240); box-shadow: rgba(15, 23, 42, 0.06) 0px 4px 16px -2px;\">', unsafe_allow_html=True)\n        st.markdown(r\"\"\"<div class=\"flex flex-col\">\n    <span class=\"font-label-sm uppercase tracking-wider text-on-surface-variant\">Importación asistida</span>")
sect2_end = content.find("        st.markdown('</section>', unsafe_allow_html=True)\n") + len("        st.markdown('</section>', unsafe_allow_html=True)\n")

if sect1_start != -1 and sect2_start != -1:
    s1 = content[sect1_start:sect1_end]
    s2 = content[sect2_start:sect2_end]
    
    # We want to change s1 to use st.expander
    # Let's rebuild s1 using native streamlit st.expander
    # The variables inside s1 are: valor_uf, dolar_val, manda_val, beneficio_val, manda_mat_val, csfj_val
    new_s1 = """
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("Ajustes Dinámicos (UF, Dólar, Beneficios)", expanded=False):
            c1, c2 = st.columns(2)
            with c1:
                valor_uf = st.number_input("Colegio SFJ (UF Base)", value=float(VALORES_BASE_MES.get("valor_uf", 37900.0)), step=10.0)
                dolar_val = st.number_input("Dólar Observado", value=VALORES_BASE_MES["valor_dolar"], step=10.0)
            with c2:
                manda_val = st.number_input("Mandarino (CLP)", value=VALORES_BASE_MES["mensualidad_mandarino"], step=1000)
                beneficio_val = st.number_input("Beneficio Empresa", value=VALORES_BASE_MES["beneficio_empleador_por_hijo"], step=1000)
                manda_mat_val = VALORES_BASE_MES.get("jardin_mandarino_materiales", 0)
        
            csfj_val = VALORES_BASE_MES.get("uf_colegio", 13.5) * valor_uf
"""
    
    # Now we piece it together: before_s1 + s2 + new_s1 + after_s2
    before_s1 = content[:sect1_start]
    after_s2 = content[sect2_end:]
    
    content = before_s1 + s2 + new_s1 + after_s2

    with open("app.py", "w") as f:
        f.write(content)
