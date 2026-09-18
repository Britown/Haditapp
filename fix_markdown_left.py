import re

with open("app.py", "r") as f:
    content = f.read()

# For the left column, we can just replace the multiline string with a clean one
old_str_2 = r"""        st.markdown(r\"\"\"
        <div style="margin-bottom: 24px;">
            <span style="font-size: 11px; font-weight: 700; letter-spacing: 0.05em; color: #86868B; text-transform: uppercase;">Importación Asistida</span>
            <h2 style="font-size: 24px; font-weight: 700; color: #1D1D1F; margin: 4px 0 0 0; letter-spacing: -0.02em;">Ingesta de Cartolas</h2>
            <p style="font-size: 13px; color: #86868B; margin: 4px 0 0 0;">Lectura inteligente con categorización semántica inmediata.</p>
        </div>
        \"\"\", unsafe_allow_html=True)"""

new_str_2 = r"""        
        left_out = r\"\"\"
        <div style="margin-bottom: 24px;">
            <span style="font-size: 11px; font-weight: 700; letter-spacing: 0.05em; color: #86868B; text-transform: uppercase;">Importación Asistida</span>
            <h2 style="font-size: 24px; font-weight: 700; color: #1D1D1F; margin: 4px 0 0 0; letter-spacing: -0.02em;">Ingesta de Cartolas</h2>
            <p style="font-size: 13px; color: #86868B; margin: 4px 0 0 0;">Lectura inteligente con categorización semántica inmediata.</p>
        </div>
        \"\"\"
        st.markdown(re.sub(r'^[ \t]+', '', left_out, flags=re.MULTILINE), unsafe_allow_html=True)"""

content = content.replace(old_str_2, new_str_2)

with open("app.py", "w") as f:
    f.write(content)
print("Fixed left column too!")
