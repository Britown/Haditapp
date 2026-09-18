with open("app.py", "r") as f:
    content = f.read()

old_icons = """                "GASTOS COMUNES": "apartment", "MANDARINO": "home_work", "ASEO": "cleaning_services",
                "INTERNET": "wifi", "VTR": "wifi", "GTD": "wifi", "CONSORCIO": "security"
            }"""

new_icons = """                "GASTOS COMUNES": "apartment", "MANDARINO": "home_work", "ASEO": "cleaning_services",
                "INTERNET": "wifi", "VTR": "wifi", "GTD": "wifi", "CONSORCIO": "security",
                "EXTRAS": "category", "CENTRO DE PADRES": "groups", "MATRÍCULA": "assignment", "MATRICULA": "assignment"
            }"""

content = content.replace(old_icons, new_icons)

with open("app.py", "w") as f:
    f.write(content)
