import re
from processor import clean_amount

raw_line = "05/08/26 0608 10679592 COLEGIO FCO.JAVIER HUECSANTIAGO $551.405 $551.405 01/01 $551.405"

line_for_amounts = raw_line.upper()
line_for_amounts = re.sub(r'\b\d{1,2}\.\d{3}\.\d{3}-[\dkK]\b', '', line_for_amounts, flags=re.IGNORECASE)
line_for_amounts = re.sub(r'\b\d{7,8}-[\dkK]\b', '', line_for_amounts, flags=re.IGNORECASE)
line_for_amounts = re.sub(r'\b\d{1,2}:\d{2}(?::\d{2})?\b', '', line_for_amounts)

amounts = []
for t in line_for_amounts.split():
    t_clean = t.strip('.,;:')
    if re.match(r'^(?:US\$|\$)?-?\d+(?:[\.\,]\d+)*$', t_clean):
        amounts.append(t_clean)

print("amounts:", amounts)

vals = []
for a in amounts:
    v = clean_amount(a)
    if v > 0: vals.append(v)
print("clean vals:", vals)

vals = [v for v in vals if v < 5000000]
print("< 5M:", vals)

vals = [v for v in vals if v >= 1000]
print(">= 1000:", vals)

if len(vals) > 1 and vals[0] <= 3112:
    vals = vals[1:]
print("after DDMM:", vals)

is_visa_quota = bool(re.search(r'\b\d{2}/\d{2}\b\s*\$\s*-?\d', raw_line))
print("is_visa_quota:", is_visa_quota)

res = vals[-1] if is_visa_quota else vals[0]
print("res:", res)
