with open("processor2.py", "r") as f:
    content = f.read()

content = content.replace("        import re\n        match = re.search", "        match = re.search")

with open("processor2.py", "w") as f:
    f.write(content)
