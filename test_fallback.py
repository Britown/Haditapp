from variables_processor import clean_fallback
desc = "03/08 Cargo por Compra en TUU*HAULMER AGREG El 3.490,00 02/08/2026 a las 13:13:33., Monto 3.490"
print("HAULMER:", clean_fallback(desc))
desc2 = "04/08 Cargo por Compra en TUU*369 BARBER ST El 25.000,00 04/08/2026 a las 13:56:07., Monto 25.000"
print("BARBER:", clean_fallback(desc2))
