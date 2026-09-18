import re

with open("app.py", "r") as f:
    content = f.read()

# Add line-height: 16px !important; to the Arrastra y suelta tus archivos aquí block
old_css = """    [data-testid="stFileUploaderDropzoneInstructions"] > div > span:nth-child(1)::after {
        content: "Arrastra y suelta tus archivos aquí";
        font-size: 12px !important;
        font-weight: 500 !important;
        color: #1D1D1F !important;
        visibility: visible;
        display: block;
        margin-bottom: 4px;
    }"""

new_css = """    [data-testid="stFileUploaderDropzoneInstructions"] > div > span:nth-child(1)::after {
        content: "Arrastra y suelta tus archivos aquí";
        font-size: 12px !important;
        line-height: 16px !important;
        font-weight: 500 !important;
        color: #1D1D1F !important;
        visibility: visible;
        display: block;
        margin-bottom: 4px;
    }"""

content = content.replace(old_css, new_css)

with open("app.py", "w") as f:
    f.write(content)
print("Line height updated")
