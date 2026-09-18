from processor import extract_all_text, process_data
from collections import namedtuple

FileObj = namedtuple('FileObj', ['name'])

# We don't have the actual PDF files, but we have the OCR text from the previous prompt!
raw_text = """
31/07 Saldo Inicial 3.836.495,00 
03/08 40197830 Cargo por transferencia a Rut 10.897.701-9 100.000,00 
04/08 Cargo por Compra en MERCADOPAGO*ELSAB El 13.500,00 2.358.400,00 
04/08/2026 a las 13:59:10., Monto 13.500 
TOTAL COMPRAS EN CUOTAS A LA CUENTA $149.805
11/08/26 1208 70961167 COMISION COMPRA INTERNACIONAL $439 $439 01/01 $439
11/08/26 PP*GOOGLE GOOGLE ONE 4029357733 US 24,93 24,93
"""

resultados, fechas, unmatched = process_data(raw_text, 950, 10000, 10000, 0)
for u in unmatched:
    print(u)
