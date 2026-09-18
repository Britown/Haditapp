import re

with open("processor.py", "r") as f:
    content = f.read()

# 1. Update amounts extraction to strip dates and RUTs
old_amounts = """        # Regex to find amounts like $100.000,00 or US$12.50 or 100.000
        amounts = re.findall(r'(?:US\\$|\\$)?\\s*-?\\d+(?:[\\.\\,]\\d+)*', line)"""

new_amounts = """        line_for_amounts = line
        if date_match:
            line_for_amounts = line.replace(date_match.group(0), '')
        # Remove RUTs
        line_for_amounts = re.sub(r'\\b\\d{1,2}\\.\\d{3}\\.\\d{3}-[\\dkK]\\b', '', line_for_amounts, flags=re.IGNORECASE)
        line_for_amounts = re.sub(r'\\b\\d{7,8}-[\\dkK]\\b', '', line_for_amounts, flags=re.IGNORECASE)
        
        # Regex to find amounts like $100.000,00 or US$12.50 or 100.000
        amounts = re.findall(r'(?:US\\$|\\$)?\\s*-?\\d+(?:[\\.\\,]\\d+)*', line_for_amounts)"""

content = content.replace(old_amounts, new_amounts)

# 2. Add upper limits to SII
content = content.replace("if val > 50000: resultados[\"CONTRIBUCIONES (SII)\"] = val", "if val > 50000 and val < 5000000: resultados[\"CONTRIBUCIONES (SII)\"] = val")

with open("processor.py", "w") as f:
    f.write(content)
