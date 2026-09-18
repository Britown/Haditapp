with open("processor2.py", "r") as f:
    content = f.read()

import re
old_func = """def get_dolar_historico(fecha, default_dolar):
    if fecha == "N/A": return default_dolar
    try:
        import requests
        if "-" in fecha:
            parts = fecha.split('-')
        else:
            parts = fecha.split('/')
            
        if len(parts) == 3:
            # Convert 26 to 2026
            if len(parts[2]) == 2:
                parts[2] = "20" + parts[2]
            formatted_date = f"{parts[0]}-{parts[1]}-{parts[2]}"
            url = f"https://mindicador.cl/api/dolar/{formatted_date}"
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                if 'serie' in data and len(data['serie']) > 0:
                    return float(data['serie'][0]['valor'])
    except:
        pass
    return default_dolar"""

new_func = """_DOLAR_CACHE = {}
def get_dolar_historico(fecha, default_dolar):
    if fecha == "N/A": return default_dolar
    
    # Simple formatting for cache key
    try:
        if "-" in fecha: parts = fecha.split('-')
        else: parts = fecha.split('/')
        if len(parts) == 3:
            if len(parts[2]) == 2: parts[2] = "20" + parts[2]
            formatted_date = f"{parts[0]}-{parts[1]}-{parts[2]}"
        else:
            return default_dolar
    except: return default_dolar

    if formatted_date in _DOLAR_CACHE:
        return _DOLAR_CACHE[formatted_date]

    try:
        import requests
        url = f"https://mindicador.cl/api/dolar/{formatted_date}"
        resp = requests.get(url, timeout=2.5)
        if resp.status_code == 200:
            data = resp.json()
            if 'serie' in data and len(data['serie']) > 0:
                val = float(data['serie'][0]['valor'])
                _DOLAR_CACHE[formatted_date] = val
                return val
    except:
        pass
        
    _DOLAR_CACHE[formatted_date] = default_dolar
    return default_dolar"""

content = content.replace(old_func, new_func)

with open("processor2.py", "w") as f:
    f.write(content)
