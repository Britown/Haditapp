with open("processor2.py", "r") as f:
    content = f.read()

old_line = "is_visa_quota = bool(re.search(r'\\b\\d{1,2}/\\d{1,2}\\b', raw_line)) or bool(re.search(r'\\b\\d+\\s+de\\s+\\d+\\b', raw_line, flags=re.IGNORECASE))"
new_line = "is_visa_quota = bool(re.search(r'\\b\\d{1,2}/\\d{1,2}\\b\\s*\\$\\s*-?\\d', raw_line)) or bool(re.search(r'\\b\\d+\\s+de\\s+\\d+\\b', raw_line, flags=re.IGNORECASE))"

content = content.replace(old_line, new_line)

with open("processor2.py", "w") as f:
    f.write(content)
