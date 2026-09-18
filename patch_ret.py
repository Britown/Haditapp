with open("processor2.py", "r") as f:
    content = f.read()

content = content.replace("return resultados, fechas, unmatched", "with open('ret_dump.txt', 'w') as fd: fd.write(str(resultados))\\n    return resultados, fechas, unmatched")

with open("processor2.py", "w") as f:
    f.write(content)
