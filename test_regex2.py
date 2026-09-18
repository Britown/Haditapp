import re
text = "0109 74987506243005252441096 Spotify P4652DD2C5 Stockholm SE 6.750,00 7,24 US$24.93"

tokens = text.split()
amounts = []
for t in tokens:
    if re.match(r'^(?:US\$|\$)?-?\d+(?:[\.\,]\d+)*$', t):
        amounts.append(t)
print(amounts)
