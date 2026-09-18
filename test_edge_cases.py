import re
from processor2 import process_data

# Simularemos un texto crudo que contiene TODAS las líneas trampa que nos han hecho tropezar.
raw_text = """
18/08 Cargo por Compra en Zapping Chile El 19.900,00 1.433.078,00
01/04/2026 Educación COLEGIO FCO.JAVIER COMPRAS NaN NaN NaN NaN 1 de 1 597626
25/03/2026 Hogar GTD MANQUEHUE S.A COMPRAS NaN NaN NaN NaN 1 de 1 34859
04/08 12397759 Transferencia de Hernan Brito Rodriguez Rut 976.598,00
10/08 Cargo por Pago Metlife Seg. Gen Nro. 108977010272. 09:00:17.978 1.030,00
Cargo por Compra en SHELL.FILE 149 P. El 55.339,00 2.214.062,00
"""

dolar_val = 950
csfj_base = 380000
manda_base = 200000
beneficio = 0

resultados, fechas, unmatch = process_data(raw_text, dolar_val, csfj_base, manda_base, beneficio)

assert resultados["ZAPPING"] == 19900.0, f"Error Zapping: {resultados['ZAPPING']}"
assert resultados["INTERNET (GTD)"] == 34859.0, f"Error GTD: {resultados['INTERNET (GTD)']}"
print("✅ TODAS LAS PRUEBAS DE CASOS DE BORDE PASARON CON ÉXITO.")
print(f"Zapping detectado: ${resultados['ZAPPING']}")
print(f"GTD detectado: ${resultados['INTERNET (GTD)']}")
import re

# Añadimos un multiline text al test
raw_text_multiline = """
31/08 13892504 Transferencia de Hernan Javier Brito 131.741,00
Rodriguez Rut 10.897.701-9 desde Banco BICE
a Khipu CL F Rut 76.187.287-7 a Cuenta
"""

resultados, fechas, unmatch = process_data(raw_text_multiline, dolar_val, csfj_base, manda_base, beneficio)
assert resultados["GASTOS COMUNES (Khipu)"] == 131741.0, f"Error Khipu: {resultados['GASTOS COMUNES (Khipu)']}"
print(f"Khipu detectado: ${resultados['GASTOS COMUNES (Khipu)']}")
