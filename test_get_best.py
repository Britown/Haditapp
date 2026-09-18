from processor_v3 import process_data
raw_text = "SANTIAGO 31/08/26 0109 10857529 AGUAS ANDINAS SANTIAGO $75.119 $75.119 01/01 $75.119"
resultados, fechas, unmatched = process_data(raw_text, 900, 0, 259400, 0)
print(resultados["AGUA (Aguas Andinas)"])
print(resultados["MANDARINO"])
