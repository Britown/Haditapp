with open("processor2.py", "r") as f:
    content = f.read()

agua_inject = """
        elif "AGUAS ANDINAS" in line_upper:
            with open("agua_debug.txt", "a") as fd: fd.write(f"AGUA line: {repr(line_upper)}\\nAMOUNTS: {amounts}\\n")
            if resultados["AGUA (Aguas Andinas)"] == 0: resultados["AGUA (Aguas Andinas)"] = get_best_amount(amounts, "AGUA (Aguas Andinas)", fecha, line_for_amounts)
"""

content = content.replace('        elif "AGUAS ANDINAS" in line_upper:\n            if resultados["AGUA (Aguas Andinas)"] == 0: resultados["AGUA (Aguas Andinas)"] = get_best_amount(amounts, "AGUA (Aguas Andinas)", fecha, line_for_amounts)', agua_inject.lstrip('\n'))

with open("processor2.py", "w") as f:
    f.write(content)
