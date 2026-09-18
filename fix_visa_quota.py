with open("processor2.py", "r") as f:
    content = f.read()

old_logic = """
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
        
        is_usd_candidate = any(x in cat.upper() for x in ["AMAZON", "HBO", "MAX", "YOUTUBE", "SPOTIFY"])
        
        if len(valid_tokens) >= 2:
            res = valid_tokens[-2]
        elif len(valid_tokens) == 1:
            res = valid_tokens[-1]
"""

new_logic = """
        is_visa_quota = bool(re.search(r'\b\d{1,2}/\d{1,2}\b', raw_line)) or bool(re.search(r'\b\d+\s+de\s+\d+\b', raw_line, flags=re.IGNORECASE))

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
        
        is_usd_candidate = any(x in cat.upper() for x in ["AMAZON", "HBO", "MAX", "YOUTUBE", "SPOTIFY"])
        
        if not valid_tokens: return 0
        
        if is_visa_quota:
            res = valid_tokens[-1]
        else:
            if len(valid_tokens) >= 2:
                res = valid_tokens[-2]
            else:
                res = valid_tokens[-1]
"""

content = content.replace(old_logic, new_logic)

with open("processor2.py", "w") as f:
    f.write(content)
