import re

lines = [
    "18/08 Cargo por Compra en Zapping Chile El 19.900,00 1.433.078,00",
    "04/08 12397759 Transferencia de Hernan Brito Rodriguez Rut 976.598,00",
    "10/08 Cargo por Pago Metlife Seg. Gen Nro. 108977010272. 09:00:17.978 1.030,00",
    "25/03/2026 Hogar GTD MANQUEHUE S.A COMPRAS NaN NaN NaN NaN 1 de 1 34859",
    "2 mar 2026 Cargos - Cargo por compra en MERCADOPAGO*EMPOR el01/03/2026 a las 18:20:04 hrs., $3.000",
    "01/04/2026 Educación COLEGIO FCO.JAVIER COMPRAS NaN NaN NaN NaN 1 de 1 597626"
]

def get_amount_from_end(line):
    # Remove quotas
    line = re.sub(r'\b\d+\s+de\s+\d+\b', ' ', line, flags=re.IGNORECASE)
    line = re.sub(r'\b\d{1,2}/\d{1,2}\b', ' ', line)
    
    # Find all numbers at the end of the line
    # A sequence of numbers separated by spaces at the end of the line
    match = re.search(r'((?:[\$\s]*[\d\.\,]+\s*)+)$', line)
    if match:
        end_str = match.group(1)
        nums = re.findall(r'[\d\.\,]+', end_str)
        # Clean nums (remove pure dots/commas)
        nums = [re.sub(r'[\.\,]', '', n) for n in nums]
        nums = [int(n) for n in nums if n.isdigit()]
        
        if len(nums) >= 2:
            # Amount is second to last! (Last is balance)
            return nums[-2]
        elif len(nums) == 1:
            return nums[-1]
    return 0

for line in lines:
    print(f"{get_amount_from_end(line)} <- {line}")
