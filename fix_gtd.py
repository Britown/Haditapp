with open("processor2.py", "r") as f:
    content = f.read()

content = content.replace('"GTD" in line_upper or "MANQUEHUE" in line_upper or "TELSUR" in line_upper', '"GTD" in line_upper or "TELSUR" in line_upper')

with open("processor2.py", "w") as f:
    f.write(content)
