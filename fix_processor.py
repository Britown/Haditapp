with open("processor2.py", "r") as f:
    content = f.read()

# Remove the nested get_best_amount
start_nested = content.find("    def get_best_amount(amounts_list, cat, fecha_str, raw_line):")
end_nested = content.find("    resultados = {", start_nested)

if start_nested != -1 and end_nested != -1:
    content = content[:start_nested] + content[end_nested:]

with open("processor2.py", "w") as f:
    f.write(content)
