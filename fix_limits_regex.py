import re

with open("processor.py", "r") as f:
    content = f.read()

# Replace val > 1000 with val > 1000 and val < 5000000 regardless of trailing spaces
content = re.sub(r'if val > 1000:\s*\n', 'if val > 1000 and val < 5000000:\n', content)
content = re.sub(r'elif val > 1000:\s*\n', 'elif val > 1000 and val < 5000000:\n', content)

with open("processor.py", "w") as f:
    f.write(content)
