import re

with open("processor2.py", "r") as f:
    content = f.read()

# We need to replace the entire `get_best_amount` function.
# Let's find its start and end.
start_idx = content.find("def get_best_amount(amounts, category_name, fecha, raw_line):")
end_idx = content.find("def clean_amount(val_str):")

new_func = """def is_valid_token(t):
    clean = re.sub(r'[\\$\\.\\,]', '', t)
    return clean.isdigit()

def get_best_amount(amounts, category_name, fecha, raw_line):
    # Remove quotas that might be glued or trick the end string
    line = re.sub(r'\\b\\d+\\s+de\\s+\\d+\\b', ' ', raw_line, flags=re.IGNORECASE)
    line = re.sub(r'\\b\\d{1,2}/\\d{1,2}\\b', ' ', line)
    
    tokens = line.split()
    if not tokens: return 0
    
    valid_tokens = []
    # Collect consecutive valid monetary tokens from the end of the line
    for t in reversed(tokens):
        if is_valid_token(t):
            valid_tokens.insert(0, clean_amount(t))
        else:
            break
            
    valid_tokens = [v for v in valid_tokens if v > 0]
    
    # Identify if it's a USD charge for specific categories
    is_usd_candidate = any(x in category_name.upper() for x in ["AMAZON", "HBO", "MAX", "YOUTUBE", "SPOTIFY"])
    
    if len(valid_tokens) >= 2:
        res = valid_tokens[-2]
    elif len(valid_tokens) == 1:
        res = valid_tokens[-1]
    else:
        # Fallback if no clean tokens at the absolute end
        raw_vals = re.findall(r'[\\d\\.\\,]+', line)
        vals = [clean_amount(v) for v in raw_vals]
        vals = [v for v in vals if v > 0]
        if not vals: return 0
        res = vals[-1]
        
    # If the amount seems like a small USD charge (e.g. $5.99 parsed as 5)
    if is_usd_candidate and res < 200:
        global _DOLAR_CACHE
        if _DOLAR_CACHE is None:
            _DOLAR_CACHE = 950 # Fallback should it fail
        res = res * _DOLAR_CACHE
        
    return res

"""

content = content[:start_idx] + new_func + content[end_idx:]

with open("processor2.py", "w") as f:
    f.write(content)
