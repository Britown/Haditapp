import re
line = "DLOCAL PRIME VIDEO SANTIAGO NaN NaN NaN NaN 1 de 1 6490"
line = re.sub(r'\b\d+\s+de\s+\d+\b', '', line, flags=re.IGNORECASE)
print(re.findall(r'[\d\.\,]+', line))
