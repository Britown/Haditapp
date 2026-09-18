import re

with open("logo_base64.txt", "r") as f:
    b64 = f.read().replace('\n', '')

with open("app.py", "r") as f:
    content = f.read()

old_h1 = """    <h1 style="font-size: 48px; font-weight: 700; color: #1D1D1F; letter-spacing: -0.04em; margin: 0; line-height: 1;">
        Hadita<span style="color: #0071E3;">.</span>
    </h1>"""

new_h1 = f"""    <div style="display: flex; align-items: center; gap: 16px;">
        <img src="data:image/png;base64,{b64}" style="height: 48px; width: auto; object-fit: contain;">
        <h1 style="font-size: 48px; font-weight: 700; color: #1D1D1F; letter-spacing: -0.04em; margin: 0; line-height: 1;">
            Hadita de las cuentas<span style="color: #0071E3;">.</span>
        </h1>
    </div>"""

content = content.replace(old_h1, new_h1)

with open("app.py", "w") as f:
    f.write(content)
print("Header updated")
