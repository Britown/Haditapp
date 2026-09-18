with open("app.py", "r") as f:
    content = f.read()

# Replace process_data if it has manda_mat_val but it's undefined
if "manda_mat_val" in content and "manda_mat_val =" not in content:
    content = content.replace("beneficio_val = st.number_input(\"Beneficio Empresa\", value=VALORES_BASE_MES[\"beneficio_empleador_por_hijo\"], step=1000)",
                              "beneficio_val = st.number_input(\"Beneficio Empresa\", value=VALORES_BASE_MES[\"beneficio_empleador_por_hijo\"], step=1000)\n            manda_mat_val = VALORES_BASE_MES.get(\"jardin_mandarino_materiales\", 0)")

with open("app.py", "w") as f:
    f.write(content)
