from processor2 import process_data

raw_text = """
15/08 YOUTUBE PREMIUM 5.990 120.000
12/08 ENEL GENERACION CHILE S.A. 45.000 0 1.500.000
10/08 ZAPPING 15.000 0 1.400.000
"""

res, fechas, un = process_data(raw_text, 950, 37900*13.5, 200000, 200000, 200000)
for k, v in res.items():
    if v > 0:
        print(f"{k}: {v}")
