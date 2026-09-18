import re

with open('config.py', 'r') as f:
    content = f.read()

# Replace mensualidad_csfj with uf_colegio and valor_uf
content = content.replace('"mensualidad_csfj": 537863,', '"uf_colegio": 13.5,\n    "valor_uf": 37900.0,')
with open('config.py', 'w') as f:
    f.write(content)
