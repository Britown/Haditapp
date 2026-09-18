import re

with open("app.py", "r") as f:
    content = f.read()

# Fix the stRadio justification safely
old_radio_css = """    div[data-testid="stRadio"] {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }"""
new_radio_css = """    div[data-testid="stRadio"] {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 20px;
    }"""
content = content.replace(old_radio_css, new_radio_css)

# Replace the Header
old_header = """st.markdown("<h1 style='text-align: center; margin-top: 10px; margin-bottom: -10px;'>Hadita</h1>", unsafe_allow_html=True)"""
new_header = r"""st.markdown(re.sub(r'^[ \t]+', '', r'''
<div style="display: flex; flex-direction: column; gap: 8px; margin-top: 16px; margin-bottom: 24px;">
    <div style="display: flex; align-items: center; gap: 8px; font-size: 11px; font-weight: 700; letter-spacing: 0.05em; color: #0071E3; text-transform: uppercase;">
        <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background-color: #0071E3;"></span>
        <span>Motor de Conciliación Bi-Familiar</span>
    </div>
    <h1 style="font-size: 48px; font-weight: 700; color: #1D1D1F; letter-spacing: -0.04em; margin: 0; line-height: 1;">
        Hadita<span style="color: #0071E3;">.</span>
    </h1>
    <p style="font-size: 15px; color: #86868B; margin: 8px 0 0 0; max-width: 600px; line-height: 1.4;">
        Conciliación financiera, mágicamente simple. Asignación transparente, lectura de extractos bancarios y balance en tiempo real.
    </p>
</div>
''', flags=re.MULTILINE), unsafe_allow_html=True)"""

content = content.replace(old_header, new_header)

with open("app.py", "w") as f:
    f.write(content)
print("Hero and radio applied cleanly")
