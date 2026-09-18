import re

with open("variables_processor.py", "r") as f:
    content = f.read()

content = content.replace('import pandas as pd', 'import pandas as pd\nfrom utils import standardize_date')

# We find where unmatched.append or items are processed and we wrap Fecha
content = content.replace('"Fecha": item["Fecha"],', '"Fecha": standardize_date(item["Fecha"]),')

with open("variables_processor.py", "w") as f:
    f.write(content)
print("variables_processor.py fixed")
