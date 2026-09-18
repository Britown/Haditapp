with open("app.py", "r") as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if "st.markdown('''<div class=\"ui-card\">" in line:
        # Instead of the card markdown, use expander
        new_lines.append("    with st.expander(\"⚙️ Ajustes Dinámicos (Variables Clave)\", expanded=False):\n")
        new_lines.append("        st.markdown(\"<div style='font-size:13px; color:#4c4546; margin-bottom:16px;'>Variables macroeconómicas y proporciones de aportes bi-familiares.</div>\", unsafe_allow_html=True)\n")
        skip = True
    elif skip and "''''', unsafe_allow_html=True)" in line:
        skip = False
    elif line.strip() == "st.markdown(\"</div>\", unsafe_allow_html=True)" and "Aporte Mamá" in lines[i-5:i]:
        # We need to find the closing div of the ui-card for this section.
        # It's right after c4, c5 and the Aporte Mamá inputs.
        pass
    else:
        if not skip:
            new_lines.append(line)

with open("app.py", "w") as f:
    f.writelines(new_lines)
