with open("app.py", "r") as f:
    content = f.read()

alert_code = """
            # --- Validacion de Gastos Fijos Obligatorios ---
            mandatory_all_year = [
                "YOUTUBE PREMIUM", "GASTOS COMUNES (Khipu)", "PISCINA (Andy)", 
                "AGUA (Aguas Andinas)", "LUZ (Enel)", "ZAPPING", "GAS (Metrogas)", 
                "SPOTIFY DUO", "INTERNET (GTD)", "SEGURO CASA (Consorcio)", "MANDARINO"
            ]
            mandatory_mar_dec = [
                "CSFJ (Mensualidad)", "CSFJ (Jornada Extendida)"
            ]
            
            missing = []
            for item in mandatory_all_year:
                if resultados.get(item, 0) == 0:
                    missing.append(item)
                    
            if sel_mes not in ["Enero", "Febrero"]:
                for item in mandatory_mar_dec:
                    if resultados.get(item, 0) == 0:
                        missing.append(item)
                        
            if missing:
                missing_str = ", ".join([f"**{m}**" for m in missing])
                st.warning(f"⚠️ **Atención:** Faltan los siguientes gastos fijos obligatorios para {sel_mes}: {missing_str}. Revisa si falta subir alguna cartola o si no se cobraron este mes.")
            # ---------------------------
"""

if "Validacion de Gastos Fijos Obligatorios" not in content:
    content = content.replace("            # ---------------------------", "            # ---------------------------" + alert_code, 1)

with open("app.py", "w") as f:
    f.write(content)
