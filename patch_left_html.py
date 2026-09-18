import re

with open("app.py", "r") as f:
    content = f.read()

# Replace the left column header HTML
old_header = """        st.markdown('<section class="bg-surface-container-lowest p-space-xl rounded-lg shadow-sm flex flex-col gap-space-lg" style="padding: 32px; background-color: rgb(255, 255, 255); border: 1px solid rgb(226, 232, 240); box-shadow: rgba(15, 23, 42, 0.06) 0px 4px 16px -2px;">', unsafe_allow_html=True)
        st.markdown(r\"\"\"<div class="flex flex-col">
    <span class="font-label-sm uppercase tracking-wider text-on-surface-variant">Importación asistida</span>
    <h2 class="font-headline-md text-headline-md text-on-surface mt-0.5">Ingesta de Cartolas</h2>
    <p class="font-body-sm text-body-sm text-on-surface-variant mt-1">
                    Lectura inteligente con categorización semántica inmediata.
                  </p>
    </div>
    <div class="w-9 h-9 rounded-full bg-surface-container-low flex items-center justify-center text-on-surface-variant">
    <span class="material-symbols-outlined text-[20px]">document_scanner</span>
    </div>
    </div>
    \"\"\", unsafe_allow_html=True)"""

new_header = """        st.markdown('<section style="background: #FFFFFF; border-radius: 24px; padding: 32px; border: 1px solid rgba(0,0,0,0.07); box-shadow: 0 4px 24px -2px rgba(0,0,0,0.04); margin-bottom: 24px;">', unsafe_allow_html=True)
        st.markdown(r\"\"\"
        <div style="margin-bottom: 24px;">
            <span style="font-size: 11px; font-weight: 700; letter-spacing: 0.05em; color: #86868B; text-transform: uppercase;">Importación Asistida</span>
            <h2 style="font-size: 24px; font-weight: 700; color: #1D1D1F; margin: 4px 0 0 0; letter-spacing: -0.02em;">Ingesta de Cartolas</h2>
            <p style="font-size: 13px; color: #86868B; margin: 4px 0 0 0;">Lectura inteligente con categorización semántica inmediata.</p>
        </div>
        \"\"\", unsafe_allow_html=True)"""

content = content.replace(old_header, new_header)

with open("app.py", "w") as f:
    f.write(content)
print("Left HTML updated!")
