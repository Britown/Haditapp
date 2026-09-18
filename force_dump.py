with open("app.py", "r") as f:
    content = f.read()

import re
content = re.sub(r'st\.info\(f"Modo Debug: Se leyeron \{len\(raw_text\)\} caracteres.*?"\)', 
                 r'\g<0>\n                with open("dump_force_res.txt", "w") as fd2: fd2.write(str(resultados))', 
                 content)

with open("app.py", "w") as f:
    f.write(content)
