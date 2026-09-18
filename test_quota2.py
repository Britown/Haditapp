import re
lines = [
    "19/08 20/08 METROGAS PAT SANTIAGO 54.481 1.433.078",
    "SANTIAGO 06/08/26 0708 11246942 ENEL SANTIAGO $202.336 $202.336 01/01 $202.336",
    "29/06/26 0309 10551638 COLEGIO FCO.JAVIER HUEC TASA INT. 2,86% $660.000 $741.780 02/06 $123.630"
]
for l in lines:
    match = re.search(r'\b\d{2}/\d{2}\b\s*\$\s*-?\d', l)
    print(f"Line: {l[:30]}... -> Quota Match: {bool(match)}")
