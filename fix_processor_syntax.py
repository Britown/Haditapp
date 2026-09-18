with open("processor.py", "r") as f:
    content = f.read()

import re
# Convert single line ifs to multi line with break
content = re.sub(r'if (val > \d+(?: and val < \d+)?):\s*(resultados\[".*?"\] = val(?:\s*\*.*?)*)\s*break',
                 r'if \1:\n                    \2\n                    break', 
                 content)

with open("processor.py", "w") as f:
    f.write(content)
