import pdfplumber
import pandas as pd
import re


_DOLAR_CACHE = {}
_API_FAILED = False
def get_dolar_historico(fecha, default_dolar):
    global _API_FAILED
    if fecha == "N/A": return default_dolar
    
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
        
    if _API_FAILED:
        _DOLAR_CACHE[formatted_date] = default_dolar
        return default_dolar

    try:
        import requests
        url = f"https://mindicador.cl/api/dolar/{formatted_date}"
        resp = requests.get(url, timeout=2.0)
        if resp.status_code == 200:
            data = resp.json()
            if 'serie' in data and len(data['serie']) > 0:
                val = float(data['serie'][0]['valor'])
                _DOLAR_CACHE[formatted_date] = val
                return val
    except:
        _API_FAILED = True
        
    _DOLAR_CACHE[formatted_date] = default_dolar
    return default_dolar

def extract_text_from_excel(file, is_csv=False):
    import pandas as pd
    try:
        if is_csv:
            df = pd.read_csv(file, sep=None, engine='python')
        else:
            df = pd.read_excel(file)
        return df.to_string(index=False, header=False, na_rep="")
    except Exception as e:
        print(f"Error procesando tabla: {e}")
        return "" 

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
            f.seek(0)
            if f.name.endswith('.pdf'):
                raw_text += "\n" + extract_text_from_pdf(f, pdf_password)
            elif f.name.endswith('.xlsx') or f.name.endswith('.xls'):
                raw_text += "\n" + extract_text_from_excel(f)
            elif f.name.endswith('.csv'):
                raw_text += "\n" + extract_text_from_excel(f, is_csv=True)
    return raw_text

def process_data(raw_text, dolar_val, csfj_base, manda_base, beneficio, manda_mat_val=220000):

    def is_valid_token(t):
        clean = t.replace('$', '').replace('.', '').replace(',', '')
        return clean.isdigit()

    def get_best_amount(amounts_list, cat, fecha_str, raw_line):
        import re
        
        is_visa_quota = bool(re.search(r'\b\d{1,2}/\d{1,2}\b\s*\$\s*-?\d', raw_line)) or bool(re.search(r'\b\d+\s+de\s+\d+\b', raw_line, flags=re.IGNORECASE))
        
        line = re.sub(r'\b\d+\s+de\s+\d+\b', ' ', raw_line, flags=re.IGNORECASE)
        line = re.sub(r'\b\d{1,2}/\d{1,2}\b', ' ', line)
        
        tokens = line.split()
        if not tokens: return 0
        
        valid_tokens = []
        for t in reversed(tokens):
            if is_valid_token(t):
                valid_tokens.insert(0, clean_amount(t))
            else:
                break
                
        valid_tokens = [v for v in valid_tokens if v > 0]
        
        is_usd_candidate = any(x in cat.upper() for x in ["AMAZON", "HBO", "MAX", "YOUTUBE", "SPOTIFY"])
        
        if not valid_tokens: 
            raw_vals = re.findall(r'[\d\.\,]+', line)
            vals = [clean_amount(v) for v in raw_vals]
            vals = [v for v in vals if v > 0]
            if not vals: return 0
            res = vals[-1]
        else:
            if is_visa_quota:
                res = valid_tokens[-1]
            else:
                if len(valid_tokens) >= 2:
                    res = valid_tokens[-2]
                else:
                    res = valid_tokens[-1]
            
        if is_usd_candidate and res < 200:
            res = res * get_dolar_historico(fecha_str, dolar_val)
            
        return res

    
    stitched_lines = []
    for line in raw_text.split('\n'):
        if not line.strip(): continue
        if re.search(r'^\s*\d{2}/\d{2}/\d{4}\s+a las', line, re.IGNORECASE) or re.search(r'^\s+(Monto|[\d\.\,]+$)', line) or re.search(r'^\s+[a-zA-Z]', line) or re.search(r'^\s*\d{2}/\d{2}/\d{4}', line):
            if stitched_lines:
                stitched_lines[-1] += " " + line.strip()
            else:
                stitched_lines.append(line.strip())
        elif re.match(r'^\d{2}/\d{2}\s', line.strip()):
            stitched_lines.append(line.strip())
        else:
            stitched_lines.append(line.strip())
    lines = stitched_lines

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
    processed_lines = set()
    
    for i, line in enumerate(lines):
        line_upper = line.upper().strip()
        if not line_upper or line_upper in processed_lines:
            continue
        processed_lines.add(line_upper)

        if "SALDO INICIAL" in line_upper or "SALDO FINAL" in line_upper or "SALDO ANTERIOR" in line_upper or "SALDO NUEVO" in line_upper or "SALDO A FAVOR" in line_upper:
            continue


        date_match = re.search(r'\b(\d{2}/\d{2}/\d{4})\b', line)
        if date_match:
            fecha = date_match.group(1)
        else:
            date_match_short = re.search(r'^(\d{2}/\d{2})\b', line)
            if date_match_short:
                # Si es 03/08 le ponemos el año actual o un placeholder para que no falle
                fecha = date_match_short.group(1) + "/2026"
            else:
                fecha = "N/A"
            
        old_resultados = resultados.copy()
        
        line_for_amounts = line
        if date_match:
            line_for_amounts = line.replace(date_match.group(0), '')
        line_for_amounts = re.sub(r'\b\d{1,2}\.\d{3}\.\d{3}-[\dkK]\b', '', line_for_amounts, flags=re.IGNORECASE)
        line_for_amounts = re.sub(r'\b\d{7,8}-[\dkK]\b', '', line_for_amounts, flags=re.IGNORECASE)
        line_for_amounts = re.sub(r'(?i)\bNro\.?\s*\d+\b', '', line_for_amounts)
        line_for_amounts = re.sub(r'(?i)\bN°\s*\d+\b', '', line_for_amounts)
        line_for_amounts = re.sub(r'\b\d{10,}\b', '', line_for_amounts) # Ignore any pure numbers longer than 9 digits (usually account/invoice numbers)

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
        elif "GTD" in line_upper or "TELSUR" in line_upper:
            if resultados["INTERNET (GTD)"] == 0: resultados["INTERNET (GTD)"] = get_best_amount(amounts, "INTERNET (GTD)", fecha, line_for_amounts)
        elif "CONSORCIO VIDA" in line_upper:
            if resultados["SEGURO CASA (Consorcio)"] == 0: resultados["SEGURO CASA (Consorcio)"] = get_best_amount(amounts, "SEGURO CASA (Consorcio)", fecha, line_for_amounts)
        elif "ZAPPING" in line_upper:
            if resultados["ZAPPING"] == 0: resultados["ZAPPING"] = get_best_amount(amounts, "ZAPPING", fecha, line_for_amounts)
        elif "AMAZON" in line_upper or "PRIME VIDEO" in line_upper:
            if resultados["AMAZON PRIME"] == 0: resultados["AMAZON PRIME"] = get_best_amount(amounts, "AMAZON PRIME", fecha, line_for_amounts)
        elif "MAX" in line_upper and ("HBO" in line_upper or "MP*MAX" in line_upper or "MERPAGO*MAX" in line_upper):
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
            
        elif "COLEGIO FCO.JAVIE" in line_upper:
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
                
                # Lookahead to catch orphaned text (like recipient names) on the next 1-2 lines
                if "Transferencia" in line or "Cargo" in line:
                    for next_idx in range(i + 1, min(i + 3, len(lines))):
                        next_line = lines[next_idx].strip()
                        if not next_line: continue
                        # Stop if the next line looks like a new transaction (has a date)
                        if re.search(r'\d{2}/\d{2}(?:/\d{4})?', next_line): break
                        # Stop if it has a large number that looks like a new amount
                        if re.search(r'\d{1,2}\.\d{3}', next_line): break
                        
                        clean_glosa += " - " + " ".join(next_line.split())
                
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


    # Post-proceso para Khipu en múltiples líneas (Cartola BICE CC)
    if resultados["GASTOS COMUNES (Khipu)"] == 0:
        match = re.search(r'Transferencia.*?([\d\.\,]+)[\s\S]{1,150}?Khipu', raw_text, flags=re.IGNORECASE)
        if match:
            amt_str = match.group(1)
            amt = clean_amount(amt_str)
            if amt > 10000:
                resultados["GASTOS COMUNES (Khipu)"] = amt
                fechas["GASTOS COMUNES (Khipu)"] = "Detectado aut."
                


            
    return resultados, fechas, unmatched


