with open("app.py", "r") as f:
    content = f.read()

import re
debug_code = """
                resultados, fechas, unmatched = process_data(raw_text, dolar_val, csfj_val, manda_val, beneficio_val, manda_mat_val)
                with open("debug_out.txt", "w") as fd:
                    fd.write(f"LEN: {len(raw_text)}\n")
                    fd.write(f"RES: {resultados}\n")
                    fd.write(f"FILES: {[f.name for f in uploaded_files]}\n")
"""
content = re.sub(r'resultados, fechas, unmatched = process_data\(raw_text, dolar_val, csfj_val, manda_val, beneficio_val, manda_mat_val\)', 
                 debug_code.strip(), 
                 content)

with open("app.py", "w") as f:
    f.write(content)
