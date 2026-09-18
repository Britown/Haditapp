import re

with open("processor.py", "r") as f:
    content = f.read()

old_logic = "amounts = re.findall(r'(?:US\\$|\\$)?\\s*-?\\d+(?:[\\.\\,]\\d+)*', line_for_amounts)"
new_logic = """amounts = []
        for t in line_for_amounts.split():
            t_clean = t.strip('.,;:')
            if re.match(r'^(?:US\\$|\\$)?-?\\d+(?:[\\.\\,]\\d+)*$', t_clean):
                amounts.append(t_clean)"""

content = content.replace(old_logic, new_logic)

with open("processor.py", "w") as f:
    f.write(content)
