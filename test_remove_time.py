import re

line = "10/08 Cargo por Pago Metlife Seg. Gen Nro. 108977010272. 09:00:17.978 1.030,00"
line = re.sub(r'\b\d{2}:\d{2}:\d{2}(?:\.\d+)?\b', ' ', line)
print(line)
