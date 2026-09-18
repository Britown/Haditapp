import re

with open("app.py", "r") as f:
    content = f.read()

# Make the CSS targeting more robust and safe
old_css = """    /* Drag and drop files here */
    [data-testid="stFileUploadDropzone"] > div > div > div > div > span {
        font-size: 0px !important;
    }
    [data-testid="stFileUploadDropzone"] > div > div > div > div > span::after {
        content: "Arrastra y suelta tus archivos aquí";
        font-size: 12px !important;
        font-weight: 500 !important;
        color: #1D1D1F !important;
        visibility: visible;
        display: block;
        margin-bottom: 4px;
    }
    
    /* Limit 200MB per file */
    [data-testid="stFileUploadDropzone"] > div > div > div > small {
        font-size: 0px !important;
    }
    [data-testid="stFileUploadDropzone"] > div > div > div > small::after {
        content: "Límite 200MB por archivo";
        font-size: 10px !important;
        color: #86868B !important;
        visibility: visible;
        display: block;
        margin-top: 4px;
    }"""

new_css = """    /* Drag and drop files here */
    [data-testid="stFileUploadDropzone"] .st-emotion-cache-1gauk5v, 
    [data-testid="stFileUploadDropzone"] span[data-testid="stMarkdownContainer"] {
        font-size: 0px !important;
    }
    [data-testid="stFileUploadDropzone"] .st-emotion-cache-1gauk5v::after,
    [data-testid="stFileUploadDropzone"] span[data-testid="stMarkdownContainer"]::after {
        content: "Arrastra y suelta tus archivos aquí";
        font-size: 12px !important;
        font-weight: 500 !important;
        color: #1D1D1F !important;
        visibility: visible;
        display: block;
        margin-bottom: 4px;
    }
    
    /* Limit 200MB per file */
    [data-testid="stFileUploadDropzone"] small {
        font-size: 0px !important;
    }
    [data-testid="stFileUploadDropzone"] small::after {
        content: "Límite 200MB por archivo";
        font-size: 10px !important;
        color: #86868B !important;
        visibility: visible;
        display: block;
        margin-top: 4px;
    }"""

content = content.replace(old_css, new_css)

with open("app.py", "w") as f:
    f.write(content)
print("Updated CSS translation rules")
