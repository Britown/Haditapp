import re
with open("app.py", "r") as f:
    content = f.read()

# Replace all occurrences of div[data-testid="stRadioGroup"] with a comma-separated list of BOTH
content = content.replace('div[data-testid="stRadioGroup"] {', 'div[data-testid="stRadio"], div[data-testid="stRadioGroup"] {')
content = content.replace('div[data-testid="stRadioGroup"] > div {', 'div[data-testid="stRadio"] > div, div[data-testid="stRadioGroup"] > div {')
content = content.replace('div[data-testid="stRadioGroup"] label {', 'div[data-testid="stRadio"] label, div[data-testid="stRadioGroup"] label {')
content = content.replace('div[data-testid="stRadioGroup"] label[data-selected="true"] {', 'div[data-testid="stRadio"] label[data-checked="true"], div[data-testid="stRadioGroup"] label[data-selected="true"] {')
content = content.replace('div[data-testid="stRadioGroup"] label:hover:not([data-checked="true"]) {', 'div[data-testid="stRadio"] label:hover:not([data-checked="true"]), div[data-testid="stRadioGroup"] label:hover:not([data-selected="true"]) {')
content = content.replace('div[data-testid="stRadioGroup"] label[data-testid="stRadioOption"] > div > div:first-child {', 'div[data-testid="stRadio"] .st-emotion-cache-1n76uvr, div[data-testid="stRadio"] .st-emotion-cache-9hdc3e, div[data-testid="stRadio"] .e1326t814, div[data-testid="stRadioGroup"] label[data-testid="stRadioOption"] > div > div:first-child {')

with open("app.py", "w") as f:
    f.write(content)
