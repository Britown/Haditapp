import re

with open("processor.py", "r") as f:
    content = f.read()

# Add benefit subtraction directly to the values at the end of process_data
old_end = """        for k in resultados:
            if resultados[k] != old_resultados[k]:
                if fechas[k] == "N/A":
                    fechas[k] = fecha
                elif fecha != "N/A" and fecha not in fechas[k]:
                    fechas[k] += f", {fecha}"

    return resultados, fechas"""

new_end = """        for k in resultados:
            if resultados[k] != old_resultados[k]:
                if fechas[k] == "N/A":
                    fechas[k] = fecha
                elif fecha != "N/A" and fecha not in fechas[k]:
                    fechas[k] += f", {fecha}"

    # Aplicar beneficio directamente a los montos de colegio/nursery
    if resultados["CSFJ (Mensualidad)"] > 0:
        resultados["CSFJ (Mensualidad)"] = max(0, resultados["CSFJ (Mensualidad)"] - beneficio)
    if resultados["MANDARINO"] > 0:
        resultados["MANDARINO"] = max(0, resultados["MANDARINO"] - beneficio)

    return resultados, fechas"""

content = content.replace(old_end, new_end)

with open("processor.py", "w") as f:
    f.write(content)

with open("app.py", "r") as f:
    app_content = f.read()

# Remove the custom logic from app.py
old_total = """            beneficios_aplicados = 0
            if beneficio_val > 0:
                if resultados.get("CSFJ (Mensualidad)", 0) > 0:
                    beneficios_aplicados += beneficio_val
                if resultados.get("MANDARINO", 0) > 0:
                    beneficios_aplicados += beneficio_val
            
            total = sum(resultados.values()) - beneficios_aplicados
            papa = int(total * FACTORES_DIVISION['PAPA'])
            mama = int(total * FACTORES_DIVISION['MAMA'])"""

new_total = """            total = sum(resultados.values())
            papa = int(total * FACTORES_DIVISION['PAPA'])
            mama = int(total * FACTORES_DIVISION['MAMA'])"""

app_content = app_content.replace(old_total, new_total)

# Remove the UI row
# The old UI row starts at "if beneficios_aplicados > 0:" and ends with '</div>\n                """'
# We can just use a regex to strip it.
app_content = re.sub(r'if beneficios_aplicados > 0:.*?</div>\n                """', '', app_content, flags=re.DOTALL)

with open("app.py", "w") as f:
    f.write(app_content)

