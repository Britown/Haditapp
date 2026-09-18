import re
line = "YOUTUBE PREMIUM 5.990 120.000"
amounts = []
for t in line.split():
    t_clean = t.strip('.,;:')
    if re.match(r'^(?:US\$|\$)?-?\d+(?:[\.\,]\d+)*$', t_clean):
        amounts.append(t_clean)
print("Amounts:", amounts)
