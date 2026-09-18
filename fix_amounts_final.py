import re

with open("processor.py", "r") as f:
    content = f.read()

old_def = """    def get_best_amount(amounts_list, cat):
        vals = []
        for a in amounts_list:
            v = clean_amount(a)
            if v > 0: vals.append(v)
        if not vals: return 0
        
        if cat in ["CSFJ (Mensualidad)", "MANDARINO"]:
            valid = [v for v in vals if v < 5000000]
            return max(valid) if valid else 0
        elif cat in ["ZAPPING", "AMAZON PRIME", "HBO MAX", "YOUTUBE PREMIUM", "SPOTIFY DUO"]:
            valid = [v for v in vals if v < 30000]
            if not valid: return 0
            res = max(valid)
            # If it's a small USD amount, convert it
            if res < 200: return res * get_dolar_historico(fecha, dolar_val)
            return res
        else:
            # Servicios basicos, seguros, etc. < 400.000
            valid = [v for v in vals if v < 400000]
            return max(valid) if valid else 0"""

new_def = """    def get_best_amount(amounts_list, cat):
        vals = []
        for a in amounts_list:
            v = clean_amount(a)
            if v > 0: vals.append(v)
            
        if not vals: return 0
        
        # Eliminar el numero de referencia (DDMM) que suele estar al inicio y es <= 3112
        if len(vals) > 1 and vals[0] <= 3112:
            vals = vals[1:]
            
        if not vals: return 0
        
        # El monto de la transaccion siempre es el primero (el ultimo suele ser el saldo)
        res = vals[0]
        
        # Si es un monto pequeño en USD (Suscripciones), lo convertimos a CLP
        if cat in ["ZAPPING", "AMAZON PRIME", "HBO MAX", "YOUTUBE PREMIUM", "SPOTIFY DUO"]:
            if res < 200: 
                return res * get_dolar_historico(fecha, dolar_val)
                
        return res"""

content = content.replace(old_def, new_def)

with open("processor.py", "w") as f:
    f.write(content)
