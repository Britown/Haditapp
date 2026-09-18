import re

with open("app.py", "r") as f:
    content = f.read()

old_total = """                        <div style="font-size: 32px; font-weight: 800; color: #1D1D1F; letter-spacing: -0.03em;">
                            $ {int(total):,}<span style="font-size: 12px; font-weight: 600; color: #86868B; margin-left: 6px;">CLP</span>
                        </div>"""

new_total = """                        <div style="font-size: 26px; font-weight: 800; color: #1D1D1F; letter-spacing: -0.03em; white-space: nowrap;">
                            $ {int(total):,}<span style="font-size: 11px; font-weight: 600; color: #86868B; margin-left: 4px;">CLP</span>
                        </div>"""

content = content.replace(old_total, new_total)

with open("app.py", "w") as f:
    f.write(content)
print("Total size updated")
