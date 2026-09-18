import re

with open("stitch_ui/code.html", "r") as f:
    html = f.read()

# Extract the tailwind config
match = re.search(r'tailwind\.config = (\{.*?\});', html, re.DOTALL)
if match:
    config_json = match.group(1)
    
    # We will modify app.py to include this config
    with open("app.py", "r") as f_app:
        app_code = f_app.read()
        
    injection = f"""
import streamlit.components.v1 as components
components.html('''
<script>
    if (!window.parent.document.getElementById('tailwind-script')) {{
        const tailwind = window.parent.document.createElement('script');
        tailwind.id = 'tailwind-script';
        tailwind.src = 'https://cdn.tailwindcss.com';
        window.parent.document.head.appendChild(tailwind);
        
        const config = window.parent.document.createElement('script');
        config.innerHTML = `tailwind.config = {{ corePlugins: {{ preflight: false }}, ...{config_json} }}`;
        window.parent.document.head.appendChild(config);
        
        const fonts = window.parent.document.createElement('link');
        fonts.rel = 'stylesheet';
        fonts.href = 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200';
        window.parent.document.head.appendChild(fonts);
    }}
</script>
''', height=0, width=0)
"""
    # Just print it for now to verify
    print("Injection ready")
