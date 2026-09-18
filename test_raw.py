with open("app.py", "r") as f:
    content = f.read()

debug = '                resultados, fechas, unmatched = process_data(raw_text, dolar_val, csfj_val, manda_val, beneficio_val, manda_mat_val)\n                with open("raw_dump.txt", "w") as fd:\n                    fd.write(raw_text)\n'

content = content.replace("                resultados, fechas, unmatched = process_data(raw_text, dolar_val, csfj_val, manda_val, beneficio_val, manda_mat_val)", debug.strip('\n'))

with open("app.py", "w") as f:
    f.write(content)
