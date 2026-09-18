import re
import textwrap

with open("app.py", "r") as f:
    content = f.read()

# Fix imports to use processor2!
content = content.replace("from processor import extract_all_text, process_data", "from processor2 import extract_all_text, process_data")

# Fix the regex for HTML block
content = content.replace("re.sub(r'^\\\\s+', '', out, flags=re.MULTILINE)", "re.sub(r'^[ \\t]+', '', out, flags=re.MULTILINE)")

with open("app.py", "w") as f:
    f.write(content)
