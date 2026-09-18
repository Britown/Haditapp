with open("processor2.py", "r") as f:
    content = f.read()

new_logic = """
        if "COLEGIO" in raw_line.upper():
            print(f"DEBUG_TOKENS: {valid_tokens}")
            print(f"DEBUG_QUOTA: {is_visa_quota}")
            
        return res
"""

content = content.replace("        if \"COLEGIO\" in raw_line.upper():\n            print(f\"DEBUG_COLEGIO: {raw_line.strip()} => {res}\")\n            \n        return res", new_logic)

with open("processor2.py", "w") as f:
    f.write(content)
