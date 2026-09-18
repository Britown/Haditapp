with open("app.py", "r") as f:
    content = f.read()

# Only do it if not already done
if 'if page == "Conciliación Fija":' not in content:
    idx_target = content.find("current_month_str =")
    if idx_target != -1:
        header_code = """
st.markdown("<h1 style='text-align: center; margin-top: 10px; margin-bottom: -10px;'>Hadita 🪄</h1>", unsafe_allow_html=True)
page = st.radio("Navegación", ["Conciliación Fija", "Gastos Variables", "Historial"], horizontal=True, label_visibility="collapsed")
st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px;'>", unsafe_allow_html=True)

if page == "Conciliación Fija":
"""
        # Indent everything from idx_target to the first elif
        idx_end = content.find("elif page == \"Gastos Variables\":")
        
        before = content[:idx_target]
        block = content[idx_target:idx_end]
        after = content[idx_end:]
        
        indented_block = "\n".join(["    " + line if line.strip() else line for line in block.split("\n")])
        
        content = before + header_code + indented_block + "\n" + after

with open("app.py", "w") as f:
    f.write(content)
