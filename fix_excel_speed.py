with open("processor2.py", "r") as f:
    content = f.read()

old_excel = """def extract_text_from_excel(file):
    df = pd.read_excel(file)
    text = ""
    for index, row in df.iterrows():
        text += " ".join([str(item) for item in row.values]) + "\\n"
    return text"""

new_excel = """def extract_text_from_excel(file, is_csv=False):
    import pandas as pd
    try:
        if is_csv:
            df = pd.read_csv(file, sep=None, engine='python')
        else:
            df = pd.read_excel(file)
        return df.to_string(index=False, header=False)
    except Exception as e:
        print(f"Error procesando tabla: {e}")
        return "" """

old_caller = """            elif f.name.endswith('.xlsx') or f.name.endswith('.xls'):
                raw_text += "\\n" + extract_text_from_excel(f)"""

new_caller = """            elif f.name.endswith('.xlsx') or f.name.endswith('.xls'):
                raw_text += "\\n" + extract_text_from_excel(f)
            elif f.name.endswith('.csv'):
                raw_text += "\\n" + extract_text_from_excel(f, is_csv=True)"""

content = content.replace(old_excel, new_excel)
content = content.replace(old_caller, new_caller)

with open("processor2.py", "w") as f:
    f.write(content)
