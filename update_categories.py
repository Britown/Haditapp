import re

with open("processor.py", "r") as f:
    content = f.read()

old_dict = """        "CSFJ (Jornada Extendida)": 0,
        "CONTRIBUCIONES (SII)": 0
    }"""

new_dict = """        "CSFJ (Jornada Extendida)": 0,
        "CSFJ (Extras/Materiales)": 0,
        "CSFJ (Centro de Padres)": 0,
        "MANDARINO (Matrícula)": 0,
        "CONTRIBUCIONES (SII)": 0
    }"""

content = content.replace(old_dict, new_dict)

with open("processor.py", "w") as f:
    f.write(content)
