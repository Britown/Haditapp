import re

with open("sheets_exporter.py", "r") as f:
    content = f.read()

content = content.replace("sheet_url", "user_email")
content = content.replace("user_email = user_email.strip()", "")

with open("sheets_exporter.py", "w") as f:
    f.write(content)

