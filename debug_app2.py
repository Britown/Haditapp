with open("app.py", "r") as f:
    content = f.read()

debug_code = """
            # BEGIN DEBUG
            st.error(f"DEBUG: csfj_base={csfj_val} | beneficio={beneficio_val}")
            st.error(f"DEBUG RESULTS: {resultados}")
            # END DEBUG
            total = sum(resultados.values())"""

if "st.error(f\"DEBUG:" in content:
    import re
    content = re.sub(r'# BEGIN DEBUG.*?# END DEBUG', debug_code.strip(), content, flags=re.DOTALL)
else:
    content = content.replace("            total = sum(resultados.values())", debug_code)

with open("app.py", "w") as f:
    f.write(content)
