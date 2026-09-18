from processor_v3 import process_data
with open("raw_dump.txt", "r") as f:
    raw_text = f.read()
resultados, fechas, unmatched = process_data(raw_text, 920, 37900*13.5, 259400, 0)
print("MANDARINO:", resultados.get("MANDARINO", "NOT FOUND"))
