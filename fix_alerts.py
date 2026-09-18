with open("app.py", "r") as f:
    content = f.read()

alerts_logic = """
                st.markdown(re.sub(r'^[ \t]+', '', out, flags=re.MULTILINE), unsafe_allow_html=True)
                st.balloons()
                
                # Alertas de gastos faltantes
                mandatory = [
                    "YOUTUBE PREMIUM", "GASTOS COMUNES (Khipu)", "PISCINA (Andy)", 
                    "AGUA (Aguas Andinas)", "LUZ (Enel)", "ZAPPING", "GAS (Metrogas)", 
                    "SPOTIFY DUO", "INTERNET (GTD)", "SEGURO CASA (Consorcio)", "MANDARINO"
                ]
                missing = []
                for m in mandatory:
                    if resultados.get(m, 0) == 0:
                        missing.append(m)
                        
                # CSFJ varies by month
                if sel_mes not in ["Enero", "Febrero"]:
                    if resultados.get("CSFJ (Mensualidad)", 0) == 0:
                        missing.append("CSFJ (Mensualidad)")
                    if resultados.get("CSFJ (Jornada Extendida)", 0) == 0:
                        missing.append("CSFJ (Jornada Extendida)")
                        
                if missing:
                    st.warning("⚠️ **Faltan los siguientes gastos obligatorios en este mes:**\\n" + "\\n".join([f"- {m}" for m in missing]))
"""

content = content.replace("                st.markdown(re.sub(r'^[ \\t]+', '', out, flags=re.MULTILINE), unsafe_allow_html=True)\n                st.balloons()", alerts_logic)

with open("app.py", "w") as f:
    f.write(content)
