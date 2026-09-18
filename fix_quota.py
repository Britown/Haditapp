import re

with open("processor.py", "r") as f:
    content = f.read()

# 1. Update signature
content = content.replace(
    'def get_best_amount(amounts_list, cat, fecha_str):',
    'def get_best_amount(amounts_list, cat, fecha_str, raw_line):'
)

# 2. Update calls
content = content.replace(', fecha)', ', fecha, line_for_amounts)')

# 3. Update the logic inside get_best_amount
old_logic = """        # El monto de la transaccion siempre es el primero que queda
        res = vals[0]"""

new_logic = """        # Identificar si es una transaccion en cuotas de la tarjeta Visa (termina en XX/YY $Monto)
        is_visa_quota = bool(re.search(r'\\b\\d{2}/\\d{2}\\b\\s*\\$\\s*-?\\d', raw_line))
        
        if is_visa_quota:
            # Si es en cuotas, el monto a pagar este mes es el ULTIMO valor de la linea
            res = vals[-1]
        else:
            # Para cuentas corrientes y compras normales, el monto es el PRIMERO que queda (antes del saldo)
            res = vals[0]"""

content = content.replace(old_logic, new_logic)

with open("processor.py", "w") as f:
    f.write(content)
