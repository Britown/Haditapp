import re

with open("processor.py", "r") as f:
    lines = f.readlines()

new_lines = []
skip_next = False
for i, line in enumerate(lines):
    if skip_next:
        skip_next = False
        continue
    
    new_lines.append(line)
    
    if "resultados[\"" in line and "val * get_dolar" not in line and "line_val = val" not in line and "MANDARINO" not in line and "GASTOS COMUNES" not in line:
        if "if val >" in line or "elif val >" in line:
            # Check if there is already a break
            if i + 1 < len(lines) and "break" in lines[i+1]:
                pass
            else:
                spaces = len(line) - len(line.lstrip())
                new_lines.append(" " * spaces + "break\n")

with open("processor.py", "w") as f:
    f.writelines(new_lines)
with open("processor.py", "r") as f:
    content = f.read()

content = content.replace("line_val = val\n", "line_val = val\n                    break\n")

with open("processor.py", "w") as f:
    f.write(content)
