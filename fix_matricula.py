import re

with open("app.py", "r") as f:
    content = f.read()

old_inputs = """    c1, c2 = st.columns(2)
    with c1:
        valor_uf = st.number_input("Colegio SFJ (UF Base)", value=float(VALORES_BASE_MES.get("valor_uf", 37900.0)), step=10.0)
        dolar_val = st.number_input("Dólar Observado", value=VALORES_BASE_MES["valor_dolar"], step=10.0)
    with c2:
        manda_val = st.number_input("Mandarino (CLP)", value=VALORES_BASE_MES["mensualidad_mandarino"], step=1000)
        beneficio_val = st.number_input("Beneficio Empresa", value=VALORES_BASE_MES["beneficio_empleador_por_hijo"], step=1000)"""

new_inputs = """    c1, c2, c3 = st.columns(3)
    with c1:
        valor_uf = st.number_input("Colegio SFJ (UF Base)", value=float(VALORES_BASE_MES.get("valor_uf", 37900.0)), step=10.0)
        dolar_val = st.number_input("Dólar Observado", value=VALORES_BASE_MES["valor_dolar"], step=10.0)
    with c2:
        manda_val = st.number_input("Mandarino (CLP)", value=VALORES_BASE_MES["mensualidad_mandarino"], step=1000)
        manda_mat_val = st.number_input("Mandarino Matrícula", value=220000, step=1000)
    with c3:
        beneficio_val = st.number_input("Beneficio Empresa", value=VALORES_BASE_MES["beneficio_empleador_por_hijo"], step=1000)"""

content = content.replace(old_inputs, new_inputs)

# Update process_data call
content = content.replace("process_data(raw_text, dolar_val, csfj_val, manda_val, beneficio_val)", 
                          "process_data(raw_text, dolar_val, csfj_val, manda_val, beneficio_val, manda_mat_val)")

with open("app.py", "w") as f:
    f.write(content)

with open("processor.py", "r") as f:
    proc = f.read()

proc = proc.replace("def process_data(raw_text, dolar_val, csfj_base, manda_base, beneficio):",
                    "def process_data(raw_text, dolar_val, csfj_base, manda_base, beneficio, manda_mat_val=220000):")

old_manda = """        elif str(int(manda_base)) in line.replace('.', ''):
            resultados["MANDARINO"] = manda_base
        elif "MANDARINO" in line_upper and "MATRICULA" in line_upper:
            for a in amounts:
                val = clean_amount(a)
                if val > 10000 and val < 5000000:
                    resultados["MANDARINO (Matrícula)"] = val
                    break"""

new_manda = """        elif str(int(manda_base)) in line.replace('.', ''):
            resultados["MANDARINO"] = manda_base
        elif str(int(manda_mat_val)) in line.replace('.', ''):
            # Check si la linea contiene la palabra cheque o simplemente asignarlo
            # ya que 220000 es un monto muy especifico.
            resultados["MANDARINO (Matrícula)"] += manda_mat_val"""

proc = proc.replace(old_manda, new_manda)

with open("processor.py", "w") as f:
    f.write(proc)

