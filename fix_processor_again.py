import re

with open("processor2.py", "r") as f:
    content = f.read()

# First, find and remove the global get_best_amount at the very bottom
start_global = content.find("def is_valid_token(t):")
if start_global != -1:
    content = content[:start_global]

# Now, we insert the robust get_best_amount inside process_data
insert_point = content.find("    resultados = {")
if insert_point == -1:
    print("Could not find insert point")

nested_func = """
    def is_valid_token(t):
        clean = t.replace('$', '').replace('.', '').replace(',', '')
        return clean.isdigit()

    def get_best_amount(amounts_list, cat, fecha_str, raw_line):
        import re
        line = re.sub(r'\\b\\d+\\s+de\\s+\\d+\\b', ' ', raw_line, flags=re.IGNORECASE)
        line = re.sub(r'\\b\\d{1,2}/\\d{1,2}\\b', ' ', line)
        
        tokens = line.split()
        if not tokens: return 0
        
        valid_tokens = []
        for t in reversed(tokens):
            if is_valid_token(t):
                valid_tokens.insert(0, clean_amount(t))
            else:
                break
                
        valid_tokens = [v for v in valid_tokens if v > 0]
        
        is_usd_candidate = any(x in cat.upper() for x in ["AMAZON", "HBO", "MAX", "YOUTUBE", "SPOTIFY"])
        
        if len(valid_tokens) >= 2:
            res = valid_tokens[-2]
        elif len(valid_tokens) == 1:
            res = valid_tokens[-1]
        else:
            raw_vals = re.findall(r'[\\d\\.\\,]+', line)
            vals = [clean_amount(v) for v in raw_vals]
            vals = [v for v in vals if v > 0]
            if not vals: return 0
            res = vals[-1]
            
        if is_usd_candidate and res < 200:
            res = res * get_dolar_historico(fecha_str, dolar_val)
            
        return res

"""

content = content[:insert_point] + nested_func + content[insert_point:]

with open("processor2.py", "w") as f:
    f.write(content)
