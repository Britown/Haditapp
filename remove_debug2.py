with open("app.py", "r") as f:
    content = f.read()

import re
content = re.sub(r'# BEGIN DEBUG.*?# END DEBUG', '', content, flags=re.DOTALL)

with open("app.py", "w") as f:
    f.write(content)
