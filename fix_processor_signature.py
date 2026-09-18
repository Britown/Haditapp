with open("processor.py", "r") as f:
    content = f.read()

old_sig = """def process_data(raw_text, dolar_val, valor_uf, manda_base, beneficio, manda_mat_val=220000):
    csfj_base = valor_uf * 13.5"""

new_sig = """def process_data(raw_text, dolar_val, csfj_base, manda_base, beneficio, manda_mat_val=220000):"""

content = content.replace(old_sig, new_sig)
with open("processor.py", "w") as f:
    f.write(content)
