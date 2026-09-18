import re

with open("app.py", "r") as f:
    content = f.read()

content = content.replace('justify-content: center;', 'justify-content: flex-start;')

with open("app.py", "w") as f:
    f.write(content)
print("Radio aligned to left")
