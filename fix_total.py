with open("app.py", "r") as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if "total = sum(resultados.values())" in line:
        if skip:
            continue
        skip = True
    new_lines.append(line)

with open("app.py", "w") as f:
    f.writelines(new_lines)
