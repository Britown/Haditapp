import re

def clean_fallback(desc):
    # Remove standard prefixes
    desc = re.sub(r'^(Cargo por Compra en|Cargo por transferencia a Rut [\d\.\-kK]+|Abono por transferencia de|Transferencia de)\s+', '', desc, flags=re.IGNORECASE)
    # Remove dates and times
    desc = re.sub(r'(?i)\s+(el|El|desde)\s+\d{2}/\d{2}/\d{4}.*$', '', desc)
    desc = re.sub(r'(?i)\s+a las\s+\d{2}:\d{2}.*$', '', desc)
    desc = re.sub(r'(?i),\s*Monto\s*[\d\.\,]+$', '', desc)
    desc = re.sub(r'(?i)\s+el\s+\d{4}-\d{2}-\d{2}.*$', '', desc)
    
    # NEW: Remove Credit Card garbage (City prefix, date prefix, auth codes)
    # e.g., "SANTIAGO 29/06/26 0309 10551638 COLEGIO" -> "COLEGIO"
    desc = re.sub(r'^(SANTIAGO|LAS CONDES|PROVIDENCIA)\s+\d{2}/\d{2}/\d{2}\s+\d{4}\s+\d+\s+', '', desc, flags=re.IGNORECASE)
    
    # NEW: Remove trailing amounts like "$660.000 $741.780 02/06 $123.630"
    desc = re.sub(r'\s*\$?\s*[\d\.\,]+\s*$', '', desc) # removes trailing amount
    desc = re.sub(r'\s+\d{2}/\d{2}\s+\$?\s*[\d\.\,]+.*$', '', desc) # removes "02/06 $123.630"
    desc = re.sub(r'\s*\$\s*[\d\.\,]+\s*\$\s*[\d\.\,]+.*$', '', desc) # removes two amounts in a row
    desc = re.sub(r'(?i)\s+TASA\s+INT\.?\s*[\d\.\,]+%.*$', '', desc) # removes TASA INT. 2,86%...
    
    return desc.strip().title()

print(clean_fallback("SANTIAGO 29/06/26 0309 10551638 COLEGIO FCO.JAVIER HUEC TASA INT. 2,86% $660.000 $741.780 02/06 $123.630"))
print(clean_fallback("SANTIAGO 12/08/25 0309 10514517 MP *MERCADO LIB TASA INT. 0,00% $313.990 $313.990 12/12 $26.175"))
