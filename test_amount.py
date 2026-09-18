import re

def is_amount(token):
    # Remove $ . , and check if digits
    clean = re.sub(r'[\$\.\,]', '', token)
    return clean.isdigit()

def extract_transaction_amount(line):
    # Remove quotas "1 de 1" or "01/12"
    line = re.sub(r'\b\d+\s+DE\s+\d+\b', ' ', line, flags=re.IGNORECASE)
    line = re.sub(r'\b\d{1,2}/\d{1,2}\b', ' ', line)
    
    tokens = line.split()
    if not tokens: return 0
    
    # Check last two tokens
    t1 = tokens[-1] if len(tokens) >= 1 else ""
    t2 = tokens[-2] if len(tokens) >= 2 else ""
    
    if is_amount(t1) and is_amount(t2):
        # Could be [Amount, Balance] or [WordNumber, Amount]
        # Balances and Amounts usually have decimals in BICE (e.g. ,00) or are large.
        # But wait! If the line is "Compra en LOCAL 123 45000"
        # t2="123", t1="45000". Both are numbers!
        # If we return t2, we return "123"! This is BAD!
        pass
    
    return 0

