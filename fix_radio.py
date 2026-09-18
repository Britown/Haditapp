import re

with open("app.py", "r") as f:
    content = f.read()

old_css = """    div[data-testid="stRadio"] .st-emotion-cache-1n76uvr { /* Hide the circle */
        display: none !important;
    }"""

new_css = """    /* Hide the circle icon next to radio labels robustly */
    div[data-testid="stRadio"] .st-emotion-cache-1n76uvr,
    div[data-testid="stRadio"] .st-emotion-cache-9hdc3e,
    div[data-testid="stRadio"] .e1326t814,
    div[data-testid="stRadio"] label > div:first-of-type:not([data-testid="stMarkdownContainer"]) {
        display: none !important;
    }"""

content = content.replace(old_css, new_css)

with open("app.py", "w") as f:
    f.write(content)
print("Radio CSS fixed")
