import re

with open("app.py", "r") as f:
    content = f.read()

# Add warnings HTML generation before rendering items
old_ui = """            # Construir items de la lista"""
new_ui = """            # Encontrar gastos no detectados
            no_detectados = [k for k, v in resultados.items() if v == 0 and not ("Matrícula" in k or "Extras" in k or "Centro de Padres" in k or "Extendida" in k)]
            warnings_html = ""
            if no_detectados:
                badges = "".join([f'<span style="display:inline-block; background:#ffe4e6; color:#be123c; padding:2px 8px; border-radius:12px; margin:2px; font-size:12px; font-weight:600;">{k}</span>' for k in no_detectados])
                warnings_html = f\"\"\"
                <div style="background-color: #fff1f2; border-left: 4px solid #e11d48; padding: 12px; border-radius: 8px; margin-bottom: 20px;">
                    <div style="display: flex; align-items: center; gap: 8px; color: #e11d48; font-weight: 600; margin-bottom: 8px;">
                        <span class="material-symbols-outlined">warning</span>
                        <span>Atención: Gastos Fijos no detectados en la cartola</span>
                    </div>
                    <div style="font-size: 13px; color: #9f1239; margin-bottom: 8px;">
                        Revisa si estos pagos se hicieron con otro medio o no han sido cobrados este mes:
                    </div>
                    <div>{badges}</div>
                </div>
                \"\"\"
            
            # Construir items de la lista"""

content = content.replace(old_ui, new_ui)

# Inject warnings_html before the items list
old_render = """<div class="flex flex-col gap-space-sm" style="gap:8px;">
                    {items_html}
                </div>"""
new_render = """{warnings_html}
                <div class="flex flex-col gap-space-sm" style="gap:8px;">
                    {items_html}
                </div>"""

content = content.replace(old_render, new_render)

with open("app.py", "w") as f:
    f.write(content)
