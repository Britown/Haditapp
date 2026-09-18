with open("app.py", "r") as f:
    content = f.read()

reload_code = """
import sys
import importlib
if 'processor2' in sys.modules:
    import processor2
    importlib.reload(processor2)
from processor2 import extract_all_text, process_data
"""
content = content.replace("from processor2 import extract_all_text, process_data", reload_code)

with open("app.py", "w") as f:
    f.write(content)
