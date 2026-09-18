import re

with open("app.py", "r") as f:
    content = f.read()

# Fix the font size of the uploader
content = content.replace('content: "Arrastra y suelta tus archivos aquí";\n        font-size: 14px !important;', 'content: "Arrastra y suelta tus archivos aquí";\n        font-size: 12px !important;')
content = content.replace('content: "Límite 200MB por archivo";\n        font-size: 12px !important;', 'content: "Límite 200MB por archivo";\n        font-size: 10px !important;')
content = content.replace('content: "Explorar archivos";\n        font-size: 13px !important;', 'content: "Explorar archivos";\n        font-size: 11px !important;')

with open("app.py", "w") as f:
    f.write(content)
print("Font sizes updated!")
