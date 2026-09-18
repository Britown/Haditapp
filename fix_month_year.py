import re
with open("app.py", "r") as f:
    content = f.read()

old_month_year = """month_year = f"{st.session_state.get('sel_mes', 'Mes')} {st.session_state.get('sel_ano', '2026')}\""""
new_month_year = """month_year = f"{sel_mes} {sel_ano}\""""

content = content.replace(old_month_year, new_month_year)
with open("app.py", "w") as f:
    f.write(content)
