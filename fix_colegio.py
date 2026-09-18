with open("processor2.py", "r") as f:
    content = f.read()

content = content.replace('elif "COLEGIO FCO.JAVIER" in line_upper:', 'elif "COLEGIO FCO.JAVIE" in line_upper:')

with open("processor2.py", "w") as f:
    f.write(content)
