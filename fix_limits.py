with open("processor.py", "r") as f:
    content = f.read()

# Replace val > 1000 with val > 1000 and val < 5000000
content = content.replace("if val > 1000:\n", "if val > 1000 and val < 5000000:\n")
content = content.replace("elif val > 1000:\n", "elif val > 1000 and val < 5000000:\n")

with open("processor.py", "w") as f:
    f.write(content)
