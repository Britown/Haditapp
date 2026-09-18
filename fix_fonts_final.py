import re

with open("app.py", "r") as f:
    content = f.read()

# Replace the font rules precisely
old_css_1 = """    /* Global font-family enforce */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif !important;
    }"""

new_css_1 = """    /* Global font-family enforce */
    html, body, [class*="css"], [class*="st-"]:not(svg):not(path) {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Protect Material Icons */
    .stIcon, .material-symbols-outlined, .material-symbols-rounded, .material-icons, 
    [data-testid="stIconMaterial"], [data-testid="stExpanderToggleIcon"] {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
    }"""

content = content.replace(old_css_1, new_css_1)

old_css_2 = """    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }"""

new_css_2 = """    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }"""

content = content.replace(old_css_2, new_css_2)

# Now fix the file uploader sizes
content = content.replace('content: "Arrastra y suelta tus archivos aquí";\n        font-size: 14px !important;', 'content: "Arrastra y suelta tus archivos aquí";\n        font-size: 12px !important;')
content = content.replace('content: "Límite 200MB por archivo";\n        font-size: 12px !important;', 'content: "Límite 200MB por archivo";\n        font-size: 10px !important;')
content = content.replace('content: "Explorar archivos";\n        font-size: 13px !important;', 'content: "Explorar archivos";\n        font-size: 12px !important;')

with open("app.py", "w") as f:
    f.write(content)
print("Font sizes and font families updated properly!")
