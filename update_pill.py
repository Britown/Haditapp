import re

with open("app.py", "r") as f:
    content = f.read()

old_loop = """            items_html = ""
            for k, v in resultados.items():
                if v > 0:
                    icon_name = get_icon(k)
                    f_val = f"{int(v):,}".replace(",", ".")
                    f_date = fechas.get(k, "Mes actual")
                    items_html += f\"\"\"
                    <div class="flex items-center justify-between p-space-md rounded-DEFAULT hover:bg-surface-container-low transition-colors" style="padding:16px; border-radius:16px;">
                        <div class="flex items-center gap-space-md min-w-0" style="gap:16px;">
                            <div class="w-10 h-10 rounded-DEFAULT bg-surface-container-low flex items-center justify-center text-on-surface-variant shrink-0" style="width:40px; height:40px; border-radius:12px; background:#f4f3f8; color:#4c4546;">
                                <span class="material-symbols-outlined text-[20px]">{icon_name}</span>
                            </div>
                            <div class="flex flex-col min-w-0">
                                <span class="font-label-lg text-label-lg text-on-surface truncate" style="font-size:15px; font-weight:600; color:#1a1b1f;">{k}</span>
                                <div class="flex items-center gap-space-xs" style="gap:4px; font-size:13px; color:#4c4546;">
                                    <span>Detectado aut.</span><span>•</span><span>{f_date}</span>
                                </div>
                            </div>
                        </div>
                        <div class="text-right">
                            <span class="font-label-lg text-label-lg text-on-surface tabular-nums" style="font-size:15px; font-weight:600; color:#1a1b1f;">$ {f_val}</span>
                        </div>
                    </div>
                    \"\"\""""

new_loop = """            items_html = ""
            for k, v in resultados.items():
                if v > 0:
                    icon_name = get_icon(k)
                    f_val = f"{int(v):,}".replace(",", ".")
                    f_date = fechas.get(k, "Mes actual")
                    
                    pill_html = ""
                    if k in ["CSFJ (Mensualidad)", "MANDARINO"] and beneficio_val > 0:
                        f_ben = f"{int(beneficio_val):,}".replace(",", ".")
                        pill_html = f'''<span style="background: #e8f5e9; color: #1b5e20; padding: 2px 8px; border-radius: 12px; font-size: 11px; margin-top: 4px; display: inline-block; font-weight: 600;">Beneficio empleado -$ {f_ben} aplicado</span>'''
                        
                    items_html += f\"\"\"
                    <div class="flex items-center justify-between p-space-md rounded-DEFAULT hover:bg-surface-container-low transition-colors" style="padding:16px; border-radius:16px;">
                        <div class="flex items-center gap-space-md min-w-0" style="gap:16px;">
                            <div class="w-10 h-10 rounded-DEFAULT bg-surface-container-low flex items-center justify-center text-on-surface-variant shrink-0" style="width:40px; height:40px; border-radius:12px; background:#f4f3f8; color:#4c4546;">
                                <span class="material-symbols-outlined text-[20px]">{icon_name}</span>
                            </div>
                            <div class="flex flex-col min-w-0">
                                <span class="font-label-lg text-label-lg text-on-surface truncate" style="font-size:15px; font-weight:600; color:#1a1b1f;">{k}</span>
                                <div class="flex items-center gap-space-xs" style="gap:4px; font-size:13px; color:#4c4546;">
                                    <span>Detectado aut.</span><span>•</span><span>{f_date}</span>
                                </div>
                                {pill_html}
                            </div>
                        </div>
                        <div class="text-right">
                            <span class="font-label-lg text-label-lg text-on-surface tabular-nums" style="font-size:15px; font-weight:600; color:#1a1b1f;">$ {f_val}</span>
                        </div>
                    </div>
                    \"\"\""""

content = content.replace(old_loop, new_loop)

with open("app.py", "w") as f:
    f.write(content)
