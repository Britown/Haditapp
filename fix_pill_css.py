with open("app.py", "r") as f:
    content = f.read()

old_pill = """pill_html = f'''<span style="background: #e8f5e9; color: #1b5e20; padding: 2px 8px; border-radius: 12px; font-size: 11px; margin-top: 4px; display: inline-block; font-weight: 600;">Beneficio empleado -$ {f_ben} aplicado</span>'''"""
new_pill = """pill_html = f'''<div style="background: #e8f5e9; color: #1b5e20; padding: 4px 8px; border-radius: 6px; font-size: 12px; margin-top: 6px; display: inline-table; font-weight: bold; width: fit-content; border: 1px solid #c8e6c9;">Beneficio empresa -$ {f_ben}</div>'''"""

content = content.replace(old_pill, new_pill)
with open("app.py", "w") as f:
    f.write(content)
