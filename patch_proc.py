with open("processor2.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    if 'resultados["MANDARINO"] = manda_base' in line:
        new_lines.append('            with open("manda_debug.txt", "a") as fd: fd.write(f"Matched manda_base {manda_base} in line: {line}\\n")\n')
    if 'resultados["MANDARINO"] = val' in line:
        new_lines.append('            with open("manda_debug.txt", "a") as fd: fd.write(f"Matched MANDARINO val {val} in line: {line}\\n")\n')

with open("processor2.py", "w") as f:
    f.writelines(new_lines)
