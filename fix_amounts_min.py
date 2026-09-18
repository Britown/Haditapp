import re

with open("processor.py", "r") as f:
    content = f.read()

old_logic = """        # Eliminar ARNs o Codigos de Autorizacion gigantes
        vals = [v for v in vals if v < 5000000]
        
        if not vals: return 0
        
        # Eliminar el numero de referencia (DDMM) que suele estar al inicio y es <= 3112
        if len(vals) > 1 and vals[0] <= 3112:
            vals = vals[1:]
            
        if not vals: return 0
        
        # El monto de la transaccion siempre es el primero que queda
        res = vals[0]
        
        # Si es un monto pequeño en USD (Suscripciones), lo convertimos a CLP
        if cat in ["ZAPPING", "AMAZON PRIME", "HBO MAX", "YOUTUBE PREMIUM", "SPOTIFY DUO"]:
            if res < 200: 
                return res * get_dolar_historico(fecha_str, dolar_val)
                
        return res"""

new_logic = """        # Eliminar ARNs o Codigos de Autorizacion gigantes
        vals = [v for v in vals if v < 5000000]
        
        is_usd_candidate = cat in ["AMAZON PRIME", "HBO MAX", "YOUTUBE PREMIUM", "SPOTIFY DUO"]
        
        # Filtrar numeros muy pequeños (basura promocional)
        if is_usd_candidate:
            # Puede ser USD (< 200) o CLP (> 1000)
            vals = [v for v in vals if (v < 200) or (v >= 1000)]
        else:
            # Zapping y cuentas basicas siempre son en CLP (> 1000)
            vals = [v for v in vals if v >= 1000]
            
        if not vals: return 0
        
        # Eliminar el numero de referencia (DDMM) que suele estar al inicio y es <= 3112
        if len(vals) > 1 and vals[0] <= 3112:
            vals = vals[1:]
            
        if not vals: return 0
        
        # El monto de la transaccion siempre es el primero que queda
        res = vals[0]
        
        if is_usd_candidate and res < 200:
            return res * get_dolar_historico(fecha_str, dolar_val)
            
        return res"""

content = content.replace(old_logic, new_logic)

with open("processor.py", "w") as f:
    f.write(content)
