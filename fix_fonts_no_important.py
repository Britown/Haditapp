import re

with open("app.py", "r") as f:
    content = f.read()

# Replace the complicated font block
old_block = """    /* Global font-family enforce - excluding icons */
    html, body, p, h1, h2, h3, h4, h5, h6, span:not(.material-symbols-outlined):not([class*="icon"]):not([class*="stIcon"]), div, button, input, select, textarea, label, a {
        font-family: 'Inter', sans-serif !important;
    }"""

new_block = """    /* Global font-family enforce */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }"""

content = content.replace(old_block, new_block)

# Replace the second font block if it exists
old_body_font = """    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }"""

new_body_font = """    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        -webkit-font-smoothing: antialiased;
    }"""

content = content.replace(old_body_font, new_body_font)

with open("app.py", "w") as f:
    f.write(content)
print("Font rules updated to remove !important")
