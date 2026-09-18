with open("app.py", "r") as f:
    content = f.read()

import re
content = re.sub(r'resultados, fechas, unmatched = process_data\(.*?\)', 
                 r'\g<0>\n                with open("dump.txt", "w") as fd: fd.write(raw_text)\n                with open("dump_res.txt", "w") as fd2: fd2.write(str(resultados))', 
                 content)

with open("app.py", "w") as f:
    f.write(content)
