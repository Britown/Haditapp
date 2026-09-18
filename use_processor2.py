with open("app.py", "r") as f:
    content = f.read()

content = content.replace("from processor import extract_all_text, process_data", "from processor2 import extract_all_text, process_data")

with open("app.py", "w") as f:
    f.write(content)
