import processor_v3

raw = """
03/08 Cargo por Compra en TUU*HAULMER AGREG El 3.490,00
      02/08/2026 a las 13:13:33., Monto 3.490
"""
res, fechas, unf = processor_v3.process_data(raw, 900, 0, 0, 0, 0)
print("UNMATCHED:")
for u in unf:
    print(u)
