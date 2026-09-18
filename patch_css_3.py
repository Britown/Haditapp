import re

with open("app.py", "r") as f:
    content = f.read()

# We need to inject the CSS into the style block
new_styles = """
    /* Global font-family enforce */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif !important;
    }
    
    /* File Uploader Translation and Typography */
    [data-testid="stFileUploadDropzone"] {
        padding: 24px !important;
        border-radius: 16px !important;
    }
    
    /* Drag and drop files here */
    [data-testid="stFileUploadDropzone"] > div > div > div > div > span {
        font-size: 0px !important;
    }
    [data-testid="stFileUploadDropzone"] > div > div > div > div > span::after {
        content: "Arrastra y suelta tus archivos aquí";
        font-size: 14px !important;
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
        font-size: 12px !important;
        color: #86868B !important;
        visibility: visible;
        display: block;
        margin-top: 4px;
    }
    
    /* Browse files button */
    [data-testid="stFileUploadDropzone"] button {
        font-size: 0px !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        border: 1px solid rgba(0,0,0,0.1) !important;
        background: #FFFFFF !important;
    }
    [data-testid="stFileUploadDropzone"] button::after {
        content: "Explorar archivos";
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #1D1D1F !important;
        visibility: visible;
    }
    [data-testid="stFileUploadDropzone"] button:hover {
        background: #F5F5F7 !important;
        border: 1px solid rgba(0,0,0,0.15) !important;
    }
"""

if "/* Global font-family enforce */" not in content:
    content = content.replace("/* Header and Title */", new_styles + "\n    /* Header and Title */")
    with open("app.py", "w") as f:
        f.write(content)
    print("CSS injected!")
else:
    print("CSS already injected")
