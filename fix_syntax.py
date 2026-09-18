with open("app.py", "r") as f:
    content = f.read()

# 1. Add Navigation and `if page == ...`
# Let's find `st.markdown(r"""<header class="fixed top-0`
target_str = 'st.markdown(r"""<header class="fixed top-0'
idx = content.find(target_str)

if idx != -1 and 'if page == "Conciliación Fija":' not in content:
    # Insert navigation
    nav = """
st.markdown("<h1 style='text-align: center; margin-top: 10px; margin-bottom: -10px;'>Hadita 🪄</h1>", unsafe_allow_html=True)
page = st.radio("Navegación", ["Conciliación Fija", "Gastos Variables", "Historial"], horizontal=True, label_visibility="collapsed")
st.markdown("<hr style='margin-top: 5px; margin-bottom: 20px;'>", unsafe_allow_html=True)

if page == "Conciliación Fija":
"""
    before = content[:idx]
    after = content[idx:]
    
    # We need to indent everything from `idx` up to the first `elif page == "Gastos Variables":`
    idx_end = after.find('elif page == "Gastos Variables":')
    
    if idx_end != -1:
        block_to_indent = after[:idx_end]
        remaining = after[idx_end:]
        
        indented_block = "\n".join(["    " + line if line.strip() else line for line in block_to_indent.split("\n")])
        
        content = before + nav + indented_block + "\n" + remaining

with open("app.py", "w") as f:
    f.write(content)
