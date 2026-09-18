from processor import process_data
text = """05/08/26 0608 10679592 COLEGIO FCO.JAVIER HUECSANTIAGO $551.405 $551.405 01/01 $551.405
29/06/26 0309 10551638 COLEGIO FCO.JAVIER HUEC TASA INT. 2,86% $660.000 $741.780 02/06 $123.630"""
resultados, fechas, unmatched = process_data(text, 950, 37900.0, 472000, 212600)
for k, v in resultados.items():
    if "CSFJ" in k:
        print(f"{k}: {v}")
