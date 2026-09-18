import re

with open("app.py", "r") as f:
    content = f.read()

start_out = content.find("out = \"\"\"\n                <section class=\"bg-surface-container-lowest")
end_out = content.find("st.markdown(re.sub(r'^[ \t]+', '', out, flags=re.MULTILINE), unsafe_allow_html=True)")

if start_out == -1 or end_out == -1:
    print(f"Could not find out block. Start: {start_out}, End: {end_out}")
    exit()

new_html_generator = '''
                # --- Right Column Apple Style HTML ---
                out = f"""
                <section style="background: #FFFFFF; border-radius: 24px; padding: 32px; border: 1px solid rgba(0,0,0,0.07); box-shadow: 0 4px 24px -2px rgba(0,0,0,0.04); margin-bottom: 24px;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid rgba(0,0,0,0.05); padding-bottom: 20px; margin-bottom: 16px;">
                        <div>
                            <span style="font-size: 11px; font-weight: 700; letter-spacing: 0.05em; color: #86868B; text-transform: uppercase;">Balance Consolidado</span>
                            <h2 style="font-size: 24px; font-weight: 700; color: #1D1D1F; margin: 4px 0 0 0; letter-spacing: -0.02em;">Desglose Detectado</h2>
                            <p style="font-size: 13px; color: #86868B; margin: 4px 0 0 0;">Gastos directos e indexados asignados a la cuenta compartida.</p>
                        </div>
                        <span style="background: #F5F5F7; color: #1D1D1F; padding: 4px 12px; border-radius: 9999px; font-size: 12px; font-weight: 600; border: 1px solid rgba(0,0,0,0.05);">
                            {len(resultados)} gastos reconocidos
                        </span>
                    </div>
                    <div style="max-height: 580px; overflow-y: auto;">
                """
                
                for k, v in resultados.items():
                    out += f"""
                    <article style="display: flex; justify-content: space-between; align-items: center; padding: 12px 8px; border-bottom: 1px solid rgba(0,0,0,0.03);">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <div style="width: 36px; height: 36px; border-radius: 50%; background: #F5F5F7; display: flex; align-items: center; justify-content: center; color: #1D1D1F;">
                                <span class="material-symbols-outlined" style="font-size: 18px;">{get_icon(k)}</span>
                            </div>
                            <div>
                                <h3 style="margin: 0; font-size: 14px; font-weight: 600; color: #1D1D1F;">{k}</h3>
                                <p style="margin: 0; font-size: 11px; color: #86868B;">Detectado aut. • {fechas.get(k, 'N/A')}</p>
                            </div>
                        </div>
                        <span style="font-size: 14px; font-weight: 600; color: #1D1D1F; letter-spacing: -0.01em;">$ {int(v):,}</span>
                    </article>
                    """.replace(",", ".")
                
                if beneficio_val > 0 and resultados.get("CSFJ (Mensualidad)", 0) > 0:
                    out += f"""
                    <article style="display: flex; justify-content: space-between; align-items: center; padding: 14px; margin-top: 16px; border-radius: 16px; background: #F0F6FF; border: 1px solid rgba(0,113,227,0.1);">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <div style="width: 36px; height: 36px; border-radius: 50%; background: #0071E3; display: flex; align-items: center; justify-content: center; color: #FFF; box-shadow: 0 2px 8px rgba(0,113,227,0.3);">
                                <span class="material-symbols-outlined" style="font-size: 18px;">redeem</span>
                            </div>
                            <div>
                                <h3 style="margin: 0; font-size: 14px; font-weight: 600; color: #0071E3;">Beneficio Empresa</h3>
                                <p style="margin: 0; font-size: 11px; color: rgba(0,113,227,0.8);">Reembolso aplicado</p>
                            </div>
                        </div>
                        <span style="font-size: 14px; font-weight: 700; color: #0071E3; letter-spacing: -0.01em;">-$ {int(beneficio_val):,}</span>
                    </article>
                    """.replace(",", ".")
                    
                papa_pct = (papa / total) * 100 if total > 0 else 0
                mama_pct = (mama / total) * 100 if total > 0 else 0

                out += f"""
                    </div>
                    
                    <div style="margin-top: 24px; padding: 24px; border-radius: 16px; background: #FAFAFC; border: 1px solid rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 11px; font-weight: 700; letter-spacing: 0.05em; color: #86868B; text-transform: uppercase;">Consolidado Actual</span>
                            <div style="font-size: 16px; font-weight: 500; color: #1D1D1F; margin-top: 2px;">Total Gastos Fijos Netos</div>
                        </div>
                        <div style="font-size: 32px; font-weight: 800; color: #1D1D1F; letter-spacing: -0.03em;">
                            $ {int(total):,}<span style="font-size: 12px; font-weight: 600; color: #86868B; margin-left: 6px;">CLP</span>
                        </div>
                    </div>
                    
                    <div style="margin-top: 24px; padding-top: 24px; border-top: 1px solid rgba(0,0,0,0.05);">
                        <div style="margin-bottom: 16px;">
                            <span style="font-size: 10px; font-weight: 700; letter-spacing: 0.05em; color: #86868B; text-transform: uppercase;">Acuerdo Bi-Parental</span>
                            <h4 style="font-size: 14px; font-weight: 700; color: #1D1D1F; margin: 4px 0 0 0;">Reparto Proporcional Acordado</h4>
                        </div>
                        
                        <div style="width: 100%; height: 10px; background: #F5F5F7; border-radius: 9999px; display: flex; overflow: hidden; margin-bottom: 20px; box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);">
                            <div style="height: 100%; background: #0071E3; width: {papa_pct}%;"></div>
                            <div style="height: 100%; background: #7C3AED; width: {mama_pct}%;"></div>
                        </div>
                        
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                            <div style="background: rgba(0,113,227,0.05); border: 1px solid rgba(0,113,227,0.15); padding: 16px; border-radius: 16px;">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                                    <div style="display: flex; align-items: center; gap: 8px;">
                                        <div style="width: 24px; height: 24px; border-radius: 50%; background: #0071E3; color: white; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700;">P</div>
                                        <span style="font-size: 12px; font-weight: 600; color: #1D1D1F;">Cuota Papá</span>
                                    </div>
                                    <span style="font-size: 11px; font-weight: 700; background: #0071E3; color: white; padding: 2px 8px; border-radius: 9999px;">{papa_pct:.2f}%</span>
                                </div>
                                <div style="font-size: 22px; font-weight: 700; color: #1D1D1F; letter-spacing: -0.02em;">$ {int(papa):,}</div>
                                <div style="font-size: 10px; color: #86868B; margin-top: 4px;">Asignación automática neta</div>
                            </div>
                            
                            <div style="background: rgba(124,58,237,0.05); border: 1px solid rgba(124,58,237,0.15); padding: 16px; border-radius: 16px;">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                                    <div style="display: flex; align-items: center; gap: 8px;">
                                        <div style="width: 24px; height: 24px; border-radius: 50%; background: #7C3AED; color: white; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700;">M</div>
                                        <span style="font-size: 12px; font-weight: 600; color: #1D1D1F;">Deuda Mamá</span>
                                    </div>
                                    <span style="font-size: 11px; font-weight: 700; background: #7C3AED; color: white; padding: 2px 8px; border-radius: 9999px;">{mama_pct:.2f}%</span>
                                </div>
                                <div style="font-size: 22px; font-weight: 700; color: #1D1D1F; letter-spacing: -0.02em;">$ {int(mama):,}</div>
                                <div style="font-size: 10px; color: #86868B; margin-top: 4px;">Por transferir a cuenta origen</div>
                            </div>
                        </div>
                    </div>
                </section>
                """.replace(",", ".")
                
                # --- End Apple Style HTML ---
'''

end_replace = end_out + len("st.markdown(re.sub(r'^[ \t]+', '', out, flags=re.MULTILINE), unsafe_allow_html=True)")

content = content[:start_out] + new_html_generator.strip('\n') + "\n                st.markdown(out, unsafe_allow_html=True)\n" + content[end_replace:]

with open("app.py", "w") as f:
    f.write(content)
print("Apple-style HTML correctly injected!")
