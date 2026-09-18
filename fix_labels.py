with open("config.py", "r") as f:
    config_content = f.read()

config_content = config_content.replace('"beneficio_empleador_por_hijo": 205200', '"beneficio_empleador_por_hijo": 212600')

with open("config.py", "w") as f:
    f.write(config_content)

with open("app.py", "r") as f:
    app_content = f.read()

app_content = app_content.replace('valor_uf = st.number_input("Colegio SFJ (UF Base)",', 'valor_uf = st.number_input("Valor UF (CLP)",')

with open("app.py", "w") as f:
    f.write(app_content)
