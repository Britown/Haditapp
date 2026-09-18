import re

with open("processor.py", "r") as f:
    content = f.read()

# Update extract_text_from_pdf
old_pdf = """def extract_text_from_pdf(file_bytes):
    text = ""
    try:
        with pdfplumber.open(file_bytes) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text: text += page_text + "\\n\""""

new_pdf = """def extract_text_from_pdf(file_bytes, pdf_password=""):
    text = ""
    try:
        if pdf_password:
            pdf = pdfplumber.open(file_bytes, password=pdf_password)
        else:
            pdf = pdfplumber.open(file_bytes)
            
        with pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text: text += page_text + "\\n\""""

content = content.replace(old_pdf, new_pdf)

# Update extract_all_text signature and call
content = content.replace("def extract_all_text(uploaded_files, pasted_text):", "def extract_all_text(uploaded_files, pasted_text, pdf_password=\"\"):")
content = content.replace("text += extract_text_from_pdf(file)", "text += extract_text_from_pdf(file, pdf_password)")

with open("processor.py", "w") as f:
    f.write(content)

with open("app.py", "r") as f:
    app_content = f.read()

# Add UI for password
old_ui = """    with c1:
        valor_uf = st.number_input("Valor UF (CLP)", value=float(VALORES_BASE_MES.get("valor_uf", 37900.0)), step=10.0)
        dolar_val = st.number_input("Dólar Observado", value=VALORES_BASE_MES["valor_dolar"], step=10.0)
    with c2:"""

new_ui = """    with c1:
        valor_uf = st.number_input("Valor UF (CLP)", value=float(VALORES_BASE_MES.get("valor_uf", 37900.0)), step=10.0)
        dolar_val = st.number_input("Dólar Observado", value=VALORES_BASE_MES["valor_dolar"], step=10.0)
        pdf_password = st.text_input("Clave PDF Banco (Opcional)", type="password", help="Si tu banco protege la cartola, ingresa tu RUT o clave aquí.")
    with c2:"""

app_content = app_content.replace(old_ui, new_ui)

# Update call
app_content = app_content.replace("raw_text = extract_all_text(uploaded_files, pasted_text)", "raw_text = extract_all_text(uploaded_files, pasted_text, pdf_password)")

with open("app.py", "w") as f:
    f.write(app_content)
