import re

def clean_fallback(desc):
    desc = re.sub(r'^(Cargo por Compra en|Cargo por transferencia a Rut [\d\.\-kK]+|Abono por transferencia de|Transferencia de)\s+', '', desc, flags=re.IGNORECASE)
    desc = re.sub(r'(?i)\s+(el|El)\s+\d{2}/\d{2}/\d{4}.*$', '', desc)
    desc = re.sub(r'(?i),\s*Monto\s*[\d\.\,]+$', '', desc)
    desc = desc.replace("  ", " ").strip().title()
    return desc
