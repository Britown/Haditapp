import re

with open("app.py", "r") as f:
    content = f.read()

# I will replace everything from /* Drag and drop files here */ down to the end of the File Uploader Translation block
old_regex = r'    /\* Drag and drop files here \*/.*?\}\n\n'

new_css = """    /* Drag and drop files here */
    [data-testid="stFileUploaderDropzoneInstructions"] > div > span:nth-child(1) {
        font-size: 0px !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] > div > span:nth-child(1)::after {
        content: "Arrastra y suelta tus archivos aquí";
        font-size: 12px !important;
        font-weight: 500 !important;
        color: #1D1D1F !important;
        visibility: visible;
        display: block;
        margin-bottom: 4px;
    }
    
    /* Limit 200MB per file */
    [data-testid="stFileUploaderDropzoneInstructions"] > div > span:nth-child(2) {
        font-size: 0px !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] > div > span:nth-child(2)::after {
        content: "Límite 200MB por archivo";
        font-size: 12px !important;
        color: #86868B !important;
        visibility: visible;
        display: block;
    }
    
    /* Browse files button */
    [data-testid="stFileUploaderDropzone"] button {
        font-size: 0px !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        border: 1px solid rgba(0,0,0,0.1) !important;
        background: #FFFFFF !important;
    }
    [data-testid="stFileUploaderDropzone"] button::after {
        content: "Explorar archivos";
        font-size: 12px !important;
        font-weight: 500 !important;
        color: #1D1D1F !important;
        visibility: visible;
    }
    [data-testid="stFileUploaderDropzone"] button:hover {
        background: #F5F5F7 !important;
        border: 1px solid rgba(0,0,0,0.15) !important;
    }

"""

content = re.sub(old_regex, new_css, content, flags=re.DOTALL)

with open("app.py", "w") as f:
    f.write(content)
print("Updated!")
