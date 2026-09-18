with open("processor2.py", "r") as f:
    content = f.read()

new_logic = """
        if "COLEGIO" in raw_line.upper():
            print(f"DEBUG_COLEGIO: {raw_line.strip()} => {res}")
            
        return res
"""

content = content.replace("        return res", new_logic)

with open("processor2.py", "w") as f:
    f.write(content)
