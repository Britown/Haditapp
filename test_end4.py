import re

lines = [
    "18/08 Cargo por Compra en Zapping Chile El 19.900,00 1.433.078,00",
    "04/08 12397759 Transferencia de Hernan Brito Rodriguez Rut 976.598,00",
    "10/08 Cargo por Pago Metlife Seg. Gen Nro. 108977010272. 09:00:17.978 1.030,00",
    "25/03/2026 Hogar GTD MANQUEHUE S.A COMPRAS NaN NaN NaN NaN 1 de 1 34859",
    "2 mar 2026 Cargos - Cargo por compra en MERCADOPAGO*EMPOR el01/03/2026 a las 18:20:04 hrs., $3.000",
    "01/04/2026 Educación COLEGIO FCO.JAVIER COMPRAS NaN NaN NaN NaN 1 de 1 597626",
    "04/08 Cargo por Compra en TUU*369 BARBER ST El 25.000,00",
    "Cargo por Compra en SHELL.FILE 149 P. El 55.339,00 2.214.062,00"
]

def clean_amount(val_str):
    val_str = val_str.replace('$', '').strip()
    if ',' in val_str:
        parts = val_str.split(',')
        if len(parts[-1]) <= 2:
            val_str = parts[0]
    val_str = val_str.replace('.', '').replace(',', '')
    try:
        return float(val_str)
    except:
        return 0

def is_valid_token(t):
    clean = re.sub(r'[\$\.\,]', '', t)
    return clean.isdigit()

def get_best(line):
    # Remove quotas 
    line = re.sub(r'\b\d+\s+de\s+\d+\b', ' ', line, flags=re.IGNORECASE)
    line = re.sub(r'\b\d{1,2}/\d{1,2}\b', ' ', line)
    
    tokens = line.split()
    if not tokens: return 0
    
    valid_tokens = []
    # Collect consecutive valid tokens from the end
    for t in reversed(tokens):
        if is_valid_token(t):
            valid_tokens.insert(0, clean_amount(t))
        else:
            break
            
    valid_tokens = [v for v in valid_tokens if v > 0]
    
    if len(valid_tokens) >= 2:
        return valid_tokens[-2]
    elif len(valid_tokens) == 1:
        return valid_tokens[-1]
        
    # Fallback to old regex logic if no pure tokens at the end
    raw_vals = re.findall(r'[\d\.\,]+', line)
    vals = [clean_amount(v) for v in raw_vals]
    vals = [v for v in vals if v > 0]
    if vals: return vals[-1]
    
    return 0

for line in lines:
    print(f"{get_best(line)} <- {line}")
