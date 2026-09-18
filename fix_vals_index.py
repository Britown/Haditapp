with open("processor2.py", "r") as f:
    content = f.read()

old_code = """        if is_visa_quota:
            # Si es en cuotas, el monto a pagar este mes es el ULTIMO valor de la linea
            res = vals[-1]
        else:
            # Para cuentas corrientes y compras normales, el monto es el PRIMERO que queda (antes del saldo)
            res = vals[0]"""

new_code = """        if is_visa_quota:
            # Si es en cuotas, el monto a pagar este mes es el ULTIMO valor de la linea
            res = vals[-1]
        else:
            # Para cuentas corrientes y compras normales, el monto suele estar al final en BICE y Excel
            res = vals[-1]"""

content = content.replace(old_code, new_code)

with open("processor2.py", "w") as f:
    f.write(content)
