with open("app.py", "r") as f:
    content = f.read()

old_total = """            total = sum(resultados.values())
            if beneficio_val > 0 and resultados.get("CSFJ (Mensualidad)", 0) > 0:
                total -= beneficio_val
            papa = int(total * FACTORES_DIVISION['PAPA'])
            mama = int(total * FACTORES_DIVISION['MAMA'])"""

new_total = """            beneficios_aplicados = 0
            if beneficio_val > 0:
                if resultados.get("CSFJ (Mensualidad)", 0) > 0:
                    beneficios_aplicados += beneficio_val
                if resultados.get("MANDARINO", 0) > 0:
                    beneficios_aplicados += beneficio_val
            
            total = sum(resultados.values()) - beneficios_aplicados
            papa = int(total * FACTORES_DIVISION['PAPA'])
            mama = int(total * FACTORES_DIVISION['MAMA'])"""

content = content.replace(old_total, new_total)

old_ui = """            if beneficio_val > 0 and resultados.get("CSFJ (Mensualidad)", 0) > 0:
                b_val = f"{int(beneficio_val):,}".replace(",", ".")
                items_html += f\"\"\"
                <div class="flex items-center justify-between p-space-md rounded-DEFAULT bg-secondary-fixed/40 hover:bg-secondary-fixed/60 transition-colors" style="padding:16px; border-radius:16px; background:rgba(218,226,255,0.4);">
                    <div class="flex items-center gap-space-md min-w-0" style="gap:16px;">
                        <div class="w-10 h-10 rounded-DEFAULT bg-secondary text-on-secondary flex items-center justify-center shrink-0" style="width:40px; height:40px; border-radius:12px; background:#dae2ff; color:#001848;">
                            <span class="material-symbols-outlined text-[20px]">redeem</span>
                        </div>
                        <div class="flex flex-col min-w-0">
                            <span class="font-label-lg text-label-lg text-secondary truncate" style="font-size:15px; font-weight:600; color:#0053cf;">Beneficio Empresa</span>
                            <div class="flex items-center gap-space-xs" style="gap:4px; font-size:13px; color:#0053cf; font-weight:500;">
                                <span>Reembolso aplicado</span>
                            </div>
                        </div>
                    </div>
                    <div class="text-right">
                        <span class="font-label-lg text-label-lg text-secondary tabular-nums" style="font-size:15px; font-weight:600; color:#0053cf;">-$ {b_val}</span>
                    </div>
                </div>
                \"\"\""""

new_ui = """            if beneficios_aplicados > 0:
                b_val = f"{int(beneficios_aplicados):,}".replace(",", ".")
                count_beneficios = int(beneficios_aplicados / beneficio_val)
                badge_text = f"Beneficio Empresa (x{count_beneficios})" if count_beneficios > 1 else "Beneficio Empresa"
                
                items_html += f\"\"\"
                <div class="flex items-center justify-between p-space-md rounded-DEFAULT bg-secondary-fixed/40 hover:bg-secondary-fixed/60 transition-colors" style="padding:16px; border-radius:16px; background:rgba(218,226,255,0.4);">
                    <div class="flex items-center gap-space-md min-w-0" style="gap:16px;">
                        <div class="w-10 h-10 rounded-DEFAULT bg-secondary text-on-secondary flex items-center justify-center shrink-0" style="width:40px; height:40px; border-radius:12px; background:#dae2ff; color:#001848;">
                            <span class="material-symbols-outlined text-[20px]">redeem</span>
                        </div>
                        <div class="flex flex-col min-w-0">
                            <span class="font-label-lg text-label-lg text-secondary truncate" style="font-size:15px; font-weight:600; color:#0053cf;">{badge_text}</span>
                            <div class="flex items-center gap-space-xs" style="gap:4px; font-size:13px; color:#0053cf; font-weight:500;">
                                <span>Reembolso aplicado al balance</span>
                            </div>
                        </div>
                    </div>
                    <div class="text-right">
                        <span class="font-label-lg text-label-lg text-secondary tabular-nums" style="font-size:15px; font-weight:600; color:#0053cf;">-$ {b_val}</span>
                    </div>
                </div>
                \"\"\""""

content = content.replace(old_ui, new_ui)

with open("app.py", "w") as f:
    f.write(content)

