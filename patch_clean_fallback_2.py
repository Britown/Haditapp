import re

with open("variables_processor.py", "r") as f:
    content = f.read()

new_clean_fallback = """
def clean_fallback(desc):
    # Remove prefix dates like "03/08 "
    desc = re.sub(r'^\d{2}/\d{2}\s+', '', desc)
    desc = re.sub(r'^(Cargo por Compra en|Cargo por transferencia a Rut [\d\.\-kK]+|Abono por transferencia de|Transferencia de)\s+', '', desc, flags=re.IGNORECASE)
    desc = re.sub(r'(?i)\s+(el|El|desde)\s+\d{2}/\d{2}/\d{4}.*$', '', desc)
    desc = re.sub(r'(?i)\s+(el|El)\s+[\d\.\,]+.*$', '', desc) # removes " El 3.490,00..."
    desc = re.sub(r'(?i)\s+a las\s+\d{2}:\d{2}.*$', '', desc)
    desc = re.sub(r'(?i),\s*Monto\s*[\d\.\,]+$', '', desc)
    desc = re.sub(r'(?i)\s+el\s+\d{4}-\d{2}-\d{2}.*$', '', desc)
    
    desc = re.sub(r'^(SANTIAGO|LAS CONDES|PROVIDENCIA)\s+\d{2}/\d{2}/\d{2}\s+\d{4}\s+\d+\s+', '', desc, flags=re.IGNORECASE)
    desc = re.sub(r'\s*\$?\s*[\d\.\,]+\s*$', '', desc)
    desc = re.sub(r'\s+\d{2}/\d{2}\s+\$?\s*[\d\.\,]+.*$', '', desc)
    desc = re.sub(r'\s*\$\s*[\d\.\,]+\s*\$\s*[\d\.\,]+.*$', '', desc)
    desc = re.sub(r'(?i)\s+TASA\s+INT\.?\s*[\d\.\,]+%.*$', '', desc)
    
    return desc.strip().title()
"""

# replace the old clean_fallback
match = re.search(r'def clean_fallback\(desc\):.*?return desc\.strip\(\)\.title\(\)', content, re.DOTALL)
if match:
    content = content.replace(match.group(0), new_clean_fallback.strip())
    with open("variables_processor.py", "w") as f:
        f.write(content)
    print("Patched!")
else:
    print("Not found")
