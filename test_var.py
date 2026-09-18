from variables_processor import process_unmatched_to_df
unmatched = [
    {"Fecha": "02/08/2026", "Descripción": "Cargo por Compra en MERPAGO*MERCADOLI El 02/08/2026 a las 19:40:40., Monto 9.476", "Monto": 9476},
    {"Fecha": "04/08/2026", "Descripción": "Abono por transferencia de VANESSA CAROLINA HERMOSILLA BERNER Rut 15.935.026-6 desde Santander el 04/08/2026 a las 11:02", "Monto": 352552}
]
df = process_unmatched_to_df(unmatched)
for idx, row in df.iterrows():
    print(row['Descripción'])
