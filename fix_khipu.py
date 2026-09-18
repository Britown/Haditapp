with open("processor2.py", "r") as f:
    content = f.read()

khipu_fix = """
    # Post-proceso para Khipu en múltiples líneas (Cartola BICE CC)
    if resultados["GASTOS COMUNES (Khipu)"] == 0:
        import re
        match = re.search(r'Transferencia.*?([\d\.\,]+)[\s\S]{1,150}?Khipu', raw_text, flags=re.IGNORECASE)
        if match:
            amt_str = match.group(1)
            amt = clean_amount(amt_str)
            if amt > 10000:
                resultados["GASTOS COMUNES (Khipu)"] = amt
                fechas["GASTOS COMUNES (Khipu)"] = "Detectado aut."
                
    return resultados, fechas, unmatched
"""

content = content.replace("    return resultados, fechas, unmatched", khipu_fix)

with open("processor2.py", "w") as f:
    f.write(content)
