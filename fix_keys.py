import re

with open("app.py", "r") as f:
    content = f.read()

# Replace the broad check with an exact check
old_check = 'if beneficio_val > 0 and ("CSFJ" in k.upper() or "MANDARINO" in k.upper()):'
new_check = 'if beneficio_val > 0 and (k == "CSFJ (Mensualidad)" or k == "MANDARINO"):'

content = content.replace(old_check, new_check)

with open("app.py", "w") as f:
    f.write(content)
