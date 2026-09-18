import re

with open("app.py", "r") as f:
    content = f.read()

old_logic = """            selected_month_num = meses.index(sel_mes) + 1
            if sum(month_counts.values()) > 0:
                predominant_month = max(month_counts, key=month_counts.get)
                if predominant_month != selected_month_num and month_counts[predominant_month] >= 2:
                    st.session_state.month_warning = f"⚠️ Las cartolas subidas parecen ser de **{meses[predominant_month - 1]}**, pero tienes seleccionado **{sel_mes}**. Asegúrate de elegir el mes correcto."
                else:
                    st.session_state.month_warning = None"""

new_logic = """            selected_month_num = meses.index(sel_mes) + 1
            if sum(month_counts.values()) > 0:
                predominant_month = max(month_counts, key=month_counts.get)
                
                # Calcular delta (considerando que Enero y Diciembre están juntos)
                delta = abs(predominant_month - selected_month_num)
                if delta > 6: delta = 12 - delta
                
                if delta > 1 and month_counts[predominant_month] >= 2:
                    st.session_state.month_warning = f"⚠️ Las cartolas subidas parecen centrarse en **{meses[predominant_month - 1]}**, pero tienes seleccionado **{sel_mes}**. Asegúrate de elegir el mes correcto."
                else:
                    st.session_state.month_warning = None"""

content = content.replace(old_logic, new_logic)

with open("app.py", "w") as f:
    f.write(content)
