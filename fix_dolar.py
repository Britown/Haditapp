import re

with open("processor.py", "r") as f:
    content = f.read()

old_func = """def get_dolar_historico(fecha, fallback_val):
    if not fecha or fecha == "N/A": 
        return fallback_val
    if fecha in dolar_cache: 
        return dolar_cache[fecha]
    
    try:
        url = f'https://mindicador.cl/api/dolar/{fecha}'
        res = requests.get(url, timeout=3)
        if res.status_code == 200:
            data = res.json()
            if data.get('serie') and len(data['serie']) > 0:
                val = float(data['serie'][0]['valor'])
                dolar_cache[fecha] = val
                return val
    except Exception:
        pass
        
    dolar_cache[fecha] = fallback_val
    return fallback_val"""

new_func = """from datetime import datetime, timedelta

def get_dolar_historico(fecha, fallback_val):
    if not fecha or fecha == "N/A": 
        return fallback_val
        
    # Formatear la fecha a DD-MM-YYYY
    try:
        # Puede venir como DD/MM/YYYY, DD-MM-YYYY, DD/MM/YY, DD-MM-YY
        parts = re.split(r'[-/]', fecha)
        if len(parts) == 3:
            day, month, year = parts
            if len(year) == 2:
                year = "20" + year
            formatted_date = f"{int(day):02d}-{int(month):02d}-{year}"
        else:
            formatted_date = fecha
    except:
        formatted_date = fecha
        
    if formatted_date in dolar_cache: 
        return dolar_cache[formatted_date]
    
    try:
        url = f'https://mindicador.cl/api/dolar/{formatted_date}'
        res = requests.get(url, timeout=3)
        if res.status_code == 200:
            data = res.json()
            if data.get('serie') and len(data['serie']) > 0:
                val = float(data['serie'][0]['valor'])
                dolar_cache[formatted_date] = val
                dolar_cache[fecha] = val # Guardar también con formato original por si acaso
                return val
    except Exception:
        pass
        
    dolar_cache[formatted_date] = fallback_val
    dolar_cache[fecha] = fallback_val
    return fallback_val"""

content = content.replace(old_func, new_func)

with open("processor.py", "w") as f:
    f.write(content)
