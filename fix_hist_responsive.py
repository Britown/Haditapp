import re

with open("app.py", "r") as f:
    content = f.read()

content = content.replace(
    '<div style="flex: 1; padding: 12px; background: white; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">',
    '<div style="flex: 1; min-width: 200px; padding: 12px; background: white; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">'
)

with open("app.py", "w") as f:
    f.write(content)
print("Historial mobile fixed")
