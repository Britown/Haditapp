import re

with open("processor.py", "r") as f:
    content = f.read()

old_logic = """        if not vals: return 0
        
        # Eliminar el numero de referencia (DDMM) que suele estar al inicio y es <= 3112
        if len(vals) > 1 and vals[0] <= 3112:
            vals = vals[1:]
            
        if not vals: return 0
        
        # El monto de la transaccion siempre es el primero que queda (el saldo esta despues)
        res = vals[0]"""

new_logic = """        # Eliminar ARNs o Codigos de Autorizacion gigantes
        vals = [v for v in vals if v < 5000000]
        
        if not vals: return 0
        
        # Eliminar el numero de referencia (DDMM) que suele estar al inicio y es <= 3112
        if len(vals) > 1 and vals[0] <= 3112:
            vals = vals[1:]
            
        if not vals: return 0
        
        # El monto de la transaccion siempre es el primero que queda
        res = vals[0]"""

content = content.replace(old_logic, new_logic)

with open("processor.py", "w") as f:
    f.write(content)
