from processor_v3 import process_data
with open("raw_dump.txt", "r") as f:
    raw_text = f.read()
resultados, fechas, unmatched = process_data(raw_text, 950, 13.5*37900, 472000, 212600, 0)
for k, v in resultados.items():
    if v > 0:
        print(f"{k}: {v}")
