with open("processor2.py", "r") as f:
    content = f.read()

if "f.seek(0)" not in content:
    content = content.replace("            if f.name.endswith('.pdf'):", "            f.seek(0)\\n            if f.name.endswith('.pdf'):")
    with open("processor2.py", "w") as f:
        f.write(content)
