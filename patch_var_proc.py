import re

with open("variables_processor.py", "r") as f:
    content = f.read()

# Make classify_variable use load_rules() dynamically
content = content.replace("for rule in RULES:", "for rule in load_rules():")

with open("variables_processor.py", "w") as f:
    f.write(content)
