from processor_v3 import process_data
from variables_processor import clean_fallback

with open("raw_dump.txt", "r") as f:
    raw_text = f.read()

resultados, fechas, unmatched = process_data(raw_text, 950, 13.5*37900, 472000, 212600, 0)

import json
items = []
for idx, u in enumerate(unmatched):
    # Try to clean it
    clean = clean_fallback(u["Descripción"])
    items.append({
        "original": u["Descripción"],
        "clean": clean,
        "monto": u["Monto"],
        "fecha": u["Fecha"]
    })

print(json.dumps(items[:10], indent=2))
