import re

with open("processor_v3.py", "r") as f:
    content = f.read()

target = r"line_for_amounts = re.sub(r'\b\d{7,8}-[\dkK]\b', '', line_for_amounts, flags=re.IGNORECASE)"

replacement = target + """
        line_for_amounts = re.sub(r'(?i)\bNro\.?\s*\d+\b', '', line_for_amounts)
        line_for_amounts = re.sub(r'(?i)\bN°\s*\d+\b', '', line_for_amounts)
        line_for_amounts = re.sub(r'\b\d{10,}\b', '', line_for_amounts) # Ignore any pure numbers longer than 9 digits (usually account/invoice numbers)
"""

content = content.replace(target, replacement)
with open("processor_v3.py", "w") as f:
    f.write(content)
