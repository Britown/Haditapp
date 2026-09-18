with open("processor2.py", "r") as f:
    content = f.read()

old_loop = """    unmatched = []
    
    for line in lines:
        line_upper = line.upper()"""

new_loop = """    unmatched = []
    processed_lines = set()
    
    for line in lines:
        line_upper = line.upper().strip()
        if not line_upper or line_upper in processed_lines:
            continue
        processed_lines.add(line_upper)"""

content = content.replace(old_loop, new_loop)

with open("processor2.py", "w") as f:
    f.write(content)
