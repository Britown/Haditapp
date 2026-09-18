with open("app.py", "r") as f:
    content = f.read()

validation_logic = """
            total = sum(resultados.values())
            
            # --- Validacion de Fechas ---
            meses_nombres = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            mes_seleccionado_num = meses_nombres.index(sel_mes) + 1
            ano_seleccionado = int(sel_ano)
            
            import re
            extracted_months = []
            for date_str in fechas.values():
                if date_str != "N/A":
                    for d in date_str.split(','):
                        d = d.strip()
                        # Formato dd/mm/yy o dd-mm-yy
                        m = re.search(r'\d{1,2}[-/](\d{1,2})[-/]\d{2,4}', d)
                        if m:
                            extracted_months.append(int(m.group(1)))
                            
            if extracted_months:
                import collections
                most_common_month = collections.Counter(extracted_months).most_common(1)[0][0]
                diff = abs(most_common_month - mes_seleccionado_num)
                # Si pasa de 12 a 1, la diff es 11. Ajuste modular:
                diff = min(diff, 12 - diff)
                
                if diff > 1:
                    st.warning(f"⚠️ **Atención:** Seleccionaste **{sel_mes} {sel_ano}**, pero la mayoría de los gastos en las cartolas parecen corresponder al mes **{most_common_month}**. Revisa si subiste el archivo correcto.")
            # ---------------------------
"""

content = content.replace("            total = sum(resultados.values())", validation_logic.lstrip('\n'))

with open("app.py", "w") as f:
    f.write(content)
