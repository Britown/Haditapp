import re

def clean_amount(monto_str):
    monto_str = monto_str.replace('$', '').replace(' ', '').replace('+', '')
    if ',' in monto_str and '.' in monto_str:
        if monto_str.rfind(',') > monto_str.rfind('.'):
            monto_str = monto_str.replace('.', '').replace(',', '.')
        else:
            monto_str = monto_str.replace(',', '')
    elif ',' in monto_str:
        if len(monto_str.split(',')[-1]) <= 2:
            monto_str = monto_str.replace(',', '.')
        else:
            monto_str = monto_str.replace(',', '')
    elif '.' in monto_str:
        if len(monto_str.split('.')[-1]) == 3:
            monto_str = monto_str.replace('.', '')
    try: return float(monto_str)
    except: return 0.0

def is_valid_token(t):
    clean = t.replace('$', '').replace('.', '').replace(',', '')
    return clean.isdigit()

def get_best_amount(cat, fecha_str, raw_line):
    is_visa_quota = bool(re.search(r'\b\d{1,2}/\d{1,2}\b\s*\$\s*-?\d', raw_line)) or bool(re.search(r'\b\d+\s+de\s+\d+\b', raw_line, flags=re.IGNORECASE))
    
    line = re.sub(r'\b\d+\s+de\s+\d+\b', ' ', raw_line, flags=re.IGNORECASE)
    line = re.sub(r'\b\d{1,2}/\d{1,2}\b', ' ', line)
    
    tokens = line.split()
    if not tokens: return 0
    
    valid_tokens = []
    for t in reversed(tokens):
        if is_valid_token(t):
            valid_tokens.insert(0, clean_amount(t))
        else:
            break
            
    valid_tokens = [v for v in valid_tokens if v > 0]
    
    print(f"is_visa_quota: {is_visa_quota}")
    print(f"valid_tokens: {valid_tokens}")
    if is_visa_quota and valid_tokens:
        return valid_tokens[-1]
    return max(valid_tokens) if valid_tokens else 0

line = "SANTIAGO 29/06/26 0309 10551638 COLEGIO FCO.JAVIER HUEC TASA INT. 2,86% $660.000 $741.780 02/06 $123.630"
print(get_best_amount("UNMATCHED", "N/A", line))
