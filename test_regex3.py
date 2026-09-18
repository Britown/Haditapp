import re
text = "0109 74987506243005252441096 Spotify P4652DD2C5 Stockholm SE 6.750,00 7,24 US$24.93 Monto: 13.500, 24.93. -100"

tokens = text.split()
amounts = []
for t in tokens:
    t_clean = t.strip('.,;:')
    if re.match(r'^(?:US\$|\$)?-?\d+(?:[\.\,]\d+)*$', t_clean):
        amounts.append(t_clean)
print(amounts)
