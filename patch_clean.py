import re

def clean_description(desc):
    # Remove prefix
    desc = re.sub(r'^(Cargo por Compra en|Cargo por transferencia a Rut [\d\.\-kK]+|Abono por transferencia de|Transferencia de)\s+', '', desc, flags=re.IGNORECASE)
    # Remove dates and anything after " el ", " El ", " a las " if it's followed by a date or time
    desc = re.sub(r'(?i)\s+(el|El|desde)\s+\d{2}/\d{2}/\d{4}.*$', '', desc)
    desc = re.sub(r'(?i)\s+a las\s+\d{2}:\d{2}.*$', '', desc)
    desc = re.sub(r'(?i),\s*Monto\s*[\d\.\,]+$', '', desc)
    desc = re.sub(r'(?i)\s+el\s+\d{4}-\d{2}-\d{2}.*$', '', desc)
    
    return desc.strip().title()

tests = [
    "Cargo por Compra en MERPAGO*MERCADOLI El 02/08/2026 a las 19:40:40., Monto 9.476",
    "Cargo por transferencia a Rut 10.897.701-9 Mercado Pago, el 03/08/2026 a las 09:00",
    "Abono por transferencia de VANESSA CAROLINA HERMOSILLA BERNER Rut 15.935.026-6 desde Santander el 04/08/2026 a las 11:02",
    "Cargo por Compra en TUU*369 BARBER ST El 04/08/2026 a las 13:56:07., Monto 25.000",
    "Transferencia de Hernan Brito Rodriguez Rut 10.897.701-9 desde Banco BICE a Hernan Brito Vidal Rut 6.847.151-6 a Cuenta Corriente de Banco de Chile-Edwards-Citi, el 2026-08-04 a las 10:39 hrs."
]

for t in tests:
    print(t)
    print("->", clean_description(t))
    print()
