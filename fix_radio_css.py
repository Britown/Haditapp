import re
with open("app.py", "r") as f:
    content = f.read()

new_css = """    /* Hide the circle icon next to radio labels robustly */
    div[data-testid="stRadioGroup"] label[data-testid="stRadioOption"] > div > div:first-child {
        display: none !important;
    }
"""

content = re.sub(
    r'/\* Hide the circle icon next to radio labels robustly \*/.*?display: none !important;\n    }',
    new_css.strip(),
    content,
    flags=re.DOTALL
)

with open("app.py", "w") as f:
    f.write(content)
