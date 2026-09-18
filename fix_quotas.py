with open("processor2.py", "r") as f:
    content = f.read()

old_code = """        else:
            line_for_amounts = line_upper
            
        # Buscar todos los montos en la linea
        amounts = re.findall(r'[\d\.\,]+', line_for_amounts)"""

new_code = """        else:
            line_for_amounts = line_upper
            
        # Limpiar cuotas tipo "1 de 3" o "01/03" para que no se confundan con montos USD
        line_for_amounts = re.sub(r'\\b\\d+\\s+DE\\s+\\d+\\b', ' ', line_for_amounts)
        line_for_amounts = re.sub(r'\\b\\d{1,2}/\\d{1,2}\\b', ' ', line_for_amounts)
            
        # Buscar todos los montos en la linea
        amounts = re.findall(r'[\\d\\.\\,]+', line_for_amounts)"""

content = content.replace(old_code, new_code)

with open("processor2.py", "w") as f:
    f.write(content)
