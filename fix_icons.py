import re

with open("app.py", "r") as f:
    content = f.read()

# I will modify the global font-family rule to explicitly exclude stIconMaterial
old_rule = """    /* Global font-family enforce */
    html, body, [class*="css"], [class*="st-"]:not(svg):not(path) {
        font-family: 'Inter', sans-serif !important;
    }"""

new_rule = """    /* Global font-family enforce */
    html, body, [class*="css"], [class*="st-"]:not(svg):not(path):not([data-testid="stIconMaterial"]):not(.material-symbols-rounded) {
        font-family: 'Inter', sans-serif !important;
    }"""

content = content.replace(old_rule, new_rule)

# Also fix the Protect Material Icons block just in case
old_protect = """    /* Protect Material Icons */
    .stIcon, .material-symbols-outlined, .material-symbols-rounded, .material-icons, 
    [data-testid="stIconMaterial"], [data-testid="stExpanderToggleIcon"] {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
    }"""

new_protect = """    /* Protect Material Icons */
    .stIcon, .material-symbols-outlined, .material-symbols-rounded, .material-icons, 
    [data-testid="stIconMaterial"], [data-testid="stExpanderToggleIcon"] {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons", sans-serif !important;
        font-weight: 400 !important;
        font-style: normal !important;
        text-transform: none !important;
        letter-spacing: normal !important;
        line-height: 1 !important;
    }"""
content = content.replace(old_protect, new_protect)

with open("app.py", "w") as f:
    f.write(content)
print("Icons fixed")
