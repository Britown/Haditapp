import re

with open("app.py", "r") as f:
    content = f.read()

old_block = """            for doc in docs:
                data = doc.to_dict()
                total = data.get('total_neto', 0)
                with st.expander(f"{doc.id} - Total: {format_clp(total)} CLP"):
                    st.json(data)"""

new_block = """            def get_icon(name):
                name = name.lower()
                if "agua" in name: return "water_drop"
                if "luz" in name or "enel" in name: return "lightbulb"
                if "gas" in name or "metrogas" in name: return "mode_heat"
                if "internet" in name or "vtr" in name or "gtd" in name: return "wifi"
                if "netflix" in name or "hbo" in name or "spotify" in name or "amazon" in name or "youtube" in name or "zapping" in name: return "play_circle"
                if "csfj" in name or "colegio" in name or "mandarino" in name: return "school"
                if "contribuciones" in name or "sii" in name: return "account_balance"
                if "seguro" in name: return "health_and_safety"
                if "gastos comunes" in name: return "location_city"
                if "aseo" in name: return "cleaning_services"
                if "piscina" in name: return "pool"
                return "receipt_long"
            
            for doc in docs:
                data = doc.to_dict()
                total = data.get('total_neto', 0)
                papa = data.get('aporte_papa', 0)
                mama = data.get('aporte_mama', 0)
                papa_pct = data.get('pct_papa', 0)
                mama_pct = data.get('pct_mama', 0)
                resultados = data.get('desglose', {})
                fechas = data.get('fechas_detectadas', {})
                
                with st.expander(f"{doc.id} - Total: {format_clp(total)} CLP"):
                    html = f'''
                    <div style="display: flex; gap: 16px; margin-bottom: 24px; padding: 16px; background: #FAFAFC; border-radius: 16px; border: 1px solid rgba(0,0,0,0.05);">
                        <div style="flex: 1; padding: 12px; background: white; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                            <div style="font-size: 11px; font-weight: 700; color: #86868B; text-transform: uppercase;">Aporte Papá ({papa_pct:.1f}%)</div>
                            <div style="font-size: 20px; font-weight: 700; color: #0071E3; margin-top: 4px;">$ {format_clp(papa)}</div>
                        </div>
                        <div style="flex: 1; padding: 12px; background: white; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                            <div style="font-size: 11px; font-weight: 700; color: #86868B; text-transform: uppercase;">Aporte Mamá ({mama_pct:.1f}%)</div>
                            <div style="font-size: 20px; font-weight: 700; color: #7C3AED; margin-top: 4px;">$ {format_clp(mama)}</div>
                        </div>
                    </div>
                    '''
                    
                    for k, v in resultados.items():
                        html += f'''
                        <article style="display: flex; justify-content: space-between; align-items: center; padding: 12px 8px; border-bottom: 1px solid rgba(0,0,0,0.03);">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div style="width: 36px; height: 36px; border-radius: 50%; background: #F5F5F7; display: flex; align-items: center; justify-content: center; color: #1D1D1F;">
                                    <span class="material-symbols-outlined" style="font-size: 18px;">{get_icon(k)}</span>
                                </div>
                                <div>
                                    <h3 style="margin: 0; font-size: 14px; font-weight: 600; color: #1D1D1F;">{k}</h3>
                                    <p style="margin: 0; font-size: 11px; color: #86868B;">Fecha: {standardize_date(fechas.get(k, 'N/A'))}</p>
                                </div>
                            </div>
                            <span style="font-size: 14px; font-weight: 600; color: #1D1D1F;">$ {format_clp(v)}</span>
                        </article>
                        '''
                    
                    st.markdown(re.sub(r'^[ \t]+', '', html, flags=re.MULTILINE), unsafe_allow_html=True)"""

content = content.replace(old_block, new_block)

with open("app.py", "w") as f:
    f.write(content)
print("Historial UI fixed")
