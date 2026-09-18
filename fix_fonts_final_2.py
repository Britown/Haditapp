import re

with open("app.py", "r") as f:
    content = f.read()

# Replace everything font related with a clean setup
new_styles = """
    /* Global font enforce */
    html, body, [class*="css"], [class*="st-"]:not(svg):not(path) {
        font-family: 'Inter', sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }
    
    /* Protect Material Icons */
    .stIcon, .material-symbols-outlined, .material-symbols-rounded, .material-icons, 
    [data-testid="stIconMaterial"],
    [data-testid="stExpanderToggleIcon"] {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
    }
"""

content = re.sub(r'    /\* Global font enforce \*/.*?    /\* Protect Material Icons \*/.*?\}', new_styles, content, flags=re.DOTALL)

with open("app.py", "w") as f:
    f.write(content)
print("Font rules updated to protect Material Icons properly")
