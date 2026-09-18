with open("app.py", "r") as f:
    content = f.read()

import re
hash_inject = """
                import hashlib
                text_hash = hashlib.sha256(raw_text.encode('utf-8')).hexdigest()
                st.info(f"Modo Debug: Se leyeron {len(raw_text)} caracteres. HASH: {text_hash[:8]}")
"""
content = re.sub(r'st\.info\(f"Modo Debug: Se leyeron \{len\(raw_text\)\} caracteres de texto de tus archivos\."\)', hash_inject, content)

with open("app.py", "w") as f:
    f.write(content)
