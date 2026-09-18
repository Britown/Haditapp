import re

with open("processor_v3.py", "r") as f:
    content = f.read()

stitch_logic = """
    stitched_lines = []
    for line in raw_text.split('\\n'):
        if not line.strip(): continue
        if re.search(r'^\s*\d{2}/\d{2}/\d{4}\s+a las', line, re.IGNORECASE) or re.search(r'^\s+(Monto|[\d\.\,]+$)', line) or re.search(r'^\s+[a-zA-Z]', line) or re.search(r'^\s*\d{2}/\d{2}/\d{4}', line):
            if stitched_lines:
                stitched_lines[-1] += " " + line.strip()
            else:
                stitched_lines.append(line.strip())
        elif re.match(r'^\d{2}/\d{2}\s', line.strip()):
            stitched_lines.append(line.strip())
        else:
            stitched_lines.append(line.strip())
    lines = stitched_lines
"""

if 'lines = raw_text.split("\\n")' in content:
    content = content.replace('lines = raw_text.split("\\n")', stitch_logic)
    
    fecha_logic = """
        date_match = re.search(r'\\b(\\d{2}/\\d{2}/\\d{4})\\b', line)
        if date_match:
            fecha = date_match.group(1)
        else:
            date_match_short = re.search(r'^(\\d{2}/\\d{2})\\b', line)
            if date_match_short:
                # Si es 03/08 le ponemos el año actual o un placeholder para que no falle
                fecha = date_match_short.group(1) + "/2026"
            else:
                fecha = "N/A"
    """
    old_fecha = """        date_match = re.search(r'\\b(\\d{1,4}[-/]\\d{1,2}[-/]\\d{1,4})\\b', line)
        fecha = date_match.group(1) if date_match else "N/A"
"""
    content = content.replace(old_fecha, fecha_logic)

    with open("processor_v3.py", "w") as f:
        f.write(content)
    print("Patched processor_v3.py successfully!")
else:
    print("Could not find lines = raw_text.split('\\n')")
