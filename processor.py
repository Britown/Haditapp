import pdfplumber
import pandas as pd
import re

def get_dolar_historico(fecha, default_dolar):
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
    return default_dolar

def extract_text_from_excel(file):
    df = pd.read_excel(file)
    text = ""
    for index, row in df.iterrows():
        text += " ".join([str(item) for item in row.values]) + "\n"
    return text

def extract_text_from_pdf(file, password=""):
    text = ""
    try:
        with pdfplumber.open(file, password=password if password else None) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text: text += page_text + "\n"
    except Exception as e:
        if "password" in str(e).lower():
            raise Exception("PDF encriptado. Por favor, ingresa la contraseña en la sección de Ajustes.")
        else:
            raise e
    return text

def clean_amount(monto_str):
    monto_str = str(monto_str).replace('US$', '').replace('$', '').replace('-', '').strip()
    if ',' in monto_str and '.' in monto_str:
        monto_str = monto_str.replace('.', '').replace(',', '.')
    elif ',' in monto_str:
        if len(monto_str.split(',')[-1]) <= 2:
            monto_str = monto_str.replace(',', '.')
        else:
            monto_str = monto_str.replace(',', '')
    elif '.' in monto_str:
        if len(monto_str.split('.')[-1]) == 3:
            monto_str = monto_str.replace('.', '')
        else:
            pass
    try:
        return float(monto_str)
    except:
        return 0.0

def extract_all_text(uploaded_files, pasted_text, pdf_password=""):
    raw_text = pasted_text or ""
    if uploaded_files:
        for f in uploaded_files:
            if f.name.endswith('.pdf'):
                raw_text += "\n" + extract_text_from_pdf(f, pdf_password)
            elif f.name.endswith('.xlsx') or f.name.endswith('.xls'):
                raw_text += "\n" + extract_text_from_excel(f)
    return raw_text

def process_data(raw_text, dolar_val, csfj_base, manda_base, beneficio, manda_mat_val=220000):
    def get_best_amount(amounts_list, cat, fecha_str, raw_line):
        vals = []
        for a in amounts_list:
            v = clean_amount(a)
            if v > 0: vals.append(v)
            
        # Eliminar ARNs o Codigos de Autorizacion gigantes
        vals = [v for v in vals if v < 5000000]
        
        is_usd_candidate = cat in ["AMAZON PRIME", "HBO MAX", "YOUTUBE PREMIUM", "SPOTIFY DUO", "UNMATCHED"]
        
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
        
        # Identificar si es una transaccion en cuotas de la tarjeta Visa (termina en XX/YY $Monto)
        is_visa_quota = bool(re.search(r'\b\d{2}/\d{2}\b\s*\$\s*-?\d', raw_line))
        
        if is_visa_quota:
            # Si es en cuotas, el monto a pagar este mes es el ULTIMO valor de la linea
            res = vals[-1]
        else:
            # Para cuentas corrientes y compras normales, el monto es el PRIMERO que queda (antes del saldo)
            res = vals[0]
        
        if is_usd_candidate and res < 200:
            return res * get_dolar_historico(fecha_str, dolar_val)
            
        return res

    text = raw_text.upper()
    lines = text.split('\n')
    
    resultados = {
        "AGUA (Aguas Andinas)": 0,
        "LUZ (Enel)": 0,
        "GAS (Metrogas)": 0,
        "INTERNET (GTD)": 0,
        "SEGURO CASA (Consorcio)": 0,
        "ZAPPING": 0,
        "AMAZON PRIME": 0,
        "HBO MAX": 0,
        "YOUTUBE PREMIUM": 0,
        "SPOTIFY DUO": 0,
        "ASEO": 0,
        "GASTOS COMUNES (Khipu)": 0,
        "PISCINA (Andy)": 0,
        "MANDARINO": 0,
        "CSFJ (Mensualidad)": 0,
        "CSFJ (Jornada Extendida)": 0,
        "CSFJ (Extras/Materiales)": 0,
        "CSFJ (Centro de Padres)": 0,
        "MANDARINO (Matrícula)": 0,
        "CONTRIBUCIONES (SII)": 0
    }
    fechas = {k: "N/A" for k in resultados}
    unmatched = []
    
    for line in lines:
        line_upper = line.upper()
        date_match = re.search(r'\b(\d{1,4}[-/]\d{1,2}[-/]\d{1,4})\b', line)
        fecha = date_match.group(1) if date_match else "N/A"
        
        old_resultados = resultados.copy()
        
        line_for_amounts = line
        if date_match:
            line_for_amounts = line.replace(date_match.group(0), '')
        line_for_amounts = re.sub(r'\b\d{1,2}\.\d{3}\.\d{3}-[\dkK]\b', '', line_for_amounts, flags=re.IGNORECASE)
        line_for_amounts = re.sub(r'\b\d{7,8}-[\dkK]\b', '', line_for_amounts, flags=re.IGNORECASE)
        # Eliminar horas para que no se confundan con montos pequeños en dolares
        line_for_amounts = re.sub(r'\b\d{1,2}:\d{2}(?::\d{2})?\b', '', line_for_amounts)
        
        amounts = []
        for t in line_for_amounts.split():
            t_clean = t.strip('.,;:')
            if re.match(r'^(?:US\$|\$)?-?\d+(?:[\.\,]\d+)*$', t_clean):
                amounts.append(t_clean)
        if not amounts:
            continue
            
        # Aseo
        if "MARISEL" in line_upper or "CAROLINA MENDOZA" in line_upper or "CRISTINA CAISALUISA" in line_upper or ("35000" in line.replace('.', '') and "TRANSFERENCIA" in line_upper):
            for a in amounts:
                val = clean_amount(a)
                if val >= 20000 and val < 5000000:
                    resultados["ASEO"] += val
                    break
            if resultados["ASEO"] == 0 and ("35000" in line.replace('.', '')):
                resultados["ASEO"] = 35000
                
        # Piscina
        elif "ANDY" in line_upper or "17.766.248-8" in line or ("27000" in line.replace('.', '') and "TRANSFERENCIA" in line_upper):
            for a in amounts:
                val = clean_amount(a)
                if val >= 15000 and val < 5000000:
                    resultados["PISCINA (Andy)"] += val
                    break
            if resultados["PISCINA (Andy)"] == 0 and ("27000" in line.replace('.', '')):
                resultados["PISCINA (Andy)"] = 27000
                
        # Mandarino
        elif "MANDARINO" in line_upper:
            val = get_best_amount(amounts, "MANDARINO", fecha, line_for_amounts)
            if val > 10000 and val < 5000000:
                resultados["MANDARINO"] = val
            if resultados["MANDARINO"] == 0:
                resultados["MANDARINO"] = manda_base
        elif manda_base > 0 and str(int(manda_base)) in line.replace('.', ''):
            resultados["MANDARINO"] = manda_base
        elif manda_mat_val > 0 and str(int(manda_mat_val)) in line.replace('.', ''):
            resultados["MANDARINO (Matrícula)"] += manda_mat_val
            
        elif "AGUAS ANDINAS" in line_upper:
            if resultados["AGUA (Aguas Andinas)"] == 0: resultados["AGUA (Aguas Andinas)"] = get_best_amount(amounts, "AGUA (Aguas Andinas)", fecha, line_for_amounts)
        elif "ENEL" in line_upper:
            if resultados["LUZ (Enel)"] == 0: resultados["LUZ (Enel)"] = get_best_amount(amounts, "LUZ (Enel)", fecha, line_for_amounts)
        elif "METROGAS" in line_upper:
            if resultados["GAS (Metrogas)"] == 0: resultados["GAS (Metrogas)"] = get_best_amount(amounts, "GAS (Metrogas)", fecha, line_for_amounts)
        elif "GTD" in line_upper or "MANQUEHUE" in line_upper or "TELSUR" in line_upper:
            if resultados["INTERNET (GTD)"] == 0: resultados["INTERNET (GTD)"] = get_best_amount(amounts, "INTERNET (GTD)", fecha, line_for_amounts)
        elif "CONSORCIO VIDA" in line_upper:
            if resultados["SEGURO CASA (Consorcio)"] == 0: resultados["SEGURO CASA (Consorcio)"] = get_best_amount(amounts, "SEGURO CASA (Consorcio)", fecha, line_for_amounts)
        elif "ZAPPING" in line_upper:
            if resultados["ZAPPING"] == 0: resultados["ZAPPING"] = get_best_amount(amounts, "ZAPPING", fecha, line_for_amounts)
        elif "AMAZON" in line_upper or "PRIME VIDEO" in line_upper:
            if resultados["AMAZON PRIME"] == 0: resultados["AMAZON PRIME"] = get_best_amount(amounts, "AMAZON PRIME", fecha, line_for_amounts)
        elif "MAX" in line_upper and ("HBO" in line_upper or "MP*MAX" in line_upper):
            if resultados["HBO MAX"] == 0: resultados["HBO MAX"] = get_best_amount(amounts, "HBO MAX", fecha, line_for_amounts)
        elif "YOUTUBE" in line_upper:
            if resultados["YOUTUBE PREMIUM"] == 0: resultados["YOUTUBE PREMIUM"] = get_best_amount(amounts, "YOUTUBE PREMIUM", fecha, line_for_amounts)
        elif "SPOTIFY" in line_upper:
            if resultados["SPOTIFY DUO"] == 0: resultados["SPOTIFY DUO"] = get_best_amount(amounts, "SPOTIFY DUO", fecha, line_for_amounts)
        elif "KHIPU" in line_upper and "CLBS" in line_upper:
            val = get_best_amount(amounts, "GASTOS COMUNES (Khipu)", fecha, line_for_amounts)
            if val > 10000: resultados["GASTOS COMUNES (Khipu)"] = val
        elif "PAGO SII" in line_upper or "CONTRIBUCIONES" in line_upper:
            val = get_best_amount(amounts, "CONTRIBUCIONES (SII)", fecha, line_for_amounts)
            if val > 10000: resultados["CONTRIBUCIONES (SII)"] = val
            
        elif "COLEGIO FCO.JAVIER" in line_upper:
            line_val = get_best_amount(amounts, "CSFJ (Mensualidad)", fecha, line_for_amounts)
            if line_val > 0:
                if "CENTRO DE PADRES" in line_upper or "CPADRES" in line_upper:
                    resultados["CSFJ (Centro de Padres)"] += line_val
                elif line_val >= csfj_base - 2000:
                    resultados["CSFJ (Mensualidad)"] = line_val if line_val < csfj_base + 2000 else csfj_base
                    if line_val > csfj_base + 2000:
                        # La diferencia (aprox 40k) suele ser materiales/seguro, no jornada extendida
                        resultados["CSFJ (Extras/Materiales)"] += (line_val - csfj_base)
                else:
                    if line_val >= 30000 and line_val <= 70000:
                        resultados["CSFJ (Extras/Materiales)"] += line_val
                    else:
                        resultados["CSFJ (Jornada Extendida)"] += line_val

        # Logic for unmatched and fechas
        cambio = False
        for k in resultados:
            if resultados[k] != old_resultados[k]:
                cambio = True
                if fechas[k] == "N/A":
                    fechas[k] = fecha
                elif fecha != "N/A" and fecha not in fechas[k]:
                    fechas[k] += f", {fecha}"
                    
        if not cambio and fecha != "N/A":
            best_val = get_best_amount(amounts, "UNMATCHED", fecha, line_for_amounts)
            if best_val > 0:
                clean_glosa = " ".join(line.split())
                unmatched.append({
                    "Fecha": fecha,
                    "Descripción": clean_glosa,
                    "Monto": best_val,
                    "Categoría": "Sin Categorizar"
                })

    if resultados["CSFJ (Mensualidad)"] > 0:
        resultados["CSFJ (Mensualidad)"] = max(0, resultados["CSFJ (Mensualidad)"] - beneficio)
    if resultados["MANDARINO"] > 0:
        resultados["MANDARINO"] = max(0, resultados["MANDARINO"] - beneficio)

    return resultados, fechas, unmatched
