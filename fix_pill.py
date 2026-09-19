import re

with open("app.py", "r") as f:
    content = f.read()

old_loop = """
                for k, v in resultados.items():
                    out += f\"\"\"
                    <article style="display: flex; justify-content: space-between; align-items: center; padding: 12px 8px; border-bottom: 1px solid rgba(0,0,0,0.03);">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <div style="width: 36px; height: 36px; border-radius: 50%; background: #F5F5F7; display: flex; align-items: center; justify-content: center; color: #1D1D1F;">
                                <span class="material-symbols-outlined" style="font-size: 18px;">{get_icon(k)}</span>
                            </div>
                            <div>
                                <h3 style="margin: 0; font-size: 14px; font-weight: 600; color: #1D1D1F;">{k}</h3>
                                <p style="margin: 0; font-size: 11px; color: #86868B;">Detectado aut. • {standardize_date(fechas.get(k, 'N/A'))}</p>
                            </div>
                        </div>
                        <span style="font-size: 14px; font-weight: 600; color: #1D1D1F; letter-spacing: -0.01em;">$ {format_clp(v)}</span>
                    </article>
                    \"\"\"
"""

new_loop = """
                for k, v in resultados.items():
                    pill_html = ""
                    if beneficio_val > 0 and ("CSFJ" in k.upper() or "MANDARINO" in k.upper()):
                        pill_html = f'''<div style="background: #e8f5e9; color: #1b5e20; padding: 2px 6px; border-radius: 4px; font-size: 10px; margin-top: 4px; display: inline-block; font-weight: 600; border: 1px solid #c8e6c9;">Beneficio empresa -$ {format_clp(beneficio_val)}</div>'''
                    
                    out += f\"\"\"
                    <article style="display: flex; justify-content: space-between; align-items: center; padding: 12px 8px; border-bottom: 1px solid rgba(0,0,0,0.03);">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <div style="width: 36px; height: 36px; border-radius: 50%; background: #F5F5F7; display: flex; align-items: center; justify-content: center; color: #1D1D1F;">
                                <span class="material-symbols-outlined" style="font-size: 18px;">{get_icon(k)}</span>
                            </div>
                            <div>
                                <h3 style="margin: 0; font-size: 14px; font-weight: 600; color: #1D1D1F;">{k}</h3>
                                <p style="margin: 0; font-size: 11px; color: #86868B;">Detectado aut. • {standardize_date(fechas.get(k, 'N/A'))}</p>
                                {pill_html}
                            </div>
                        </div>
                        <span style="font-size: 14px; font-weight: 600; color: #1D1D1F; letter-spacing: -0.01em;">$ {format_clp(v)}</span>
                    </article>
                    \"\"\"
"""

content = content.replace(old_loop.strip(), new_loop.strip())

with open("app.py", "w") as f:
    f.write(content)
