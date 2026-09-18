import re

with open("processor2.py", "r") as f:
    content = f.read()

# We need to locate the definition of get_best_amount
start_idx = content.find("    def get_best_amount(amounts_list, cat, fecha_str, raw_line):")
end_idx = content.find("    lines = raw_text.split(\"\\n\")")

new_func = """    def get_best_amount(amounts_list, cat, fecha_str, raw_line):
        import re
        
        is_visa_quota = bool(re.search(r'\\b\\d{1,2}/\\d{1,2}\\b', raw_line)) or bool(re.search(r'\\b\\d+\\s+de\\s+\\d+\\b', raw_line, flags=re.IGNORECASE))
        
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
        
        if not valid_tokens: 
            raw_vals = re.findall(r'[\\d\\.\\,]+', line)
            vals = [clean_amount(v) for v in raw_vals]
            vals = [v for v in vals if v > 0]
            if not vals: return 0
            res = vals[-1]
        else:
            if is_visa_quota:
                res = valid_tokens[-1]
            else:
                if len(valid_tokens) >= 2:
                    res = valid_tokens[-2]
                else:
                    res = valid_tokens[-1]
            
        if is_usd_candidate and res < 200:
            res = res * get_dolar_historico(fecha_str, dolar_val)
            
        return res

"""

content = content[:start_idx] + new_func + content[end_idx:]

with open("processor2.py", "w") as f:
    f.write(content)
