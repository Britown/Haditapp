with open("app.py", "r") as f:
    content = f.read()

# Find the block from components.html down to """, height=0, width=0)
import re
new_script = """components.html(\"\"\"
<script>
    if (!window.parent.document.getElementById('material-fonts-script')) {
        const fonts = window.parent.document.createElement('link');
        fonts.id = 'material-fonts-script';
        fonts.rel = 'stylesheet';
        fonts.href = 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200';
        window.parent.document.head.appendChild(fonts);
    }
</script>
\"\"\", height=0, width=0)"""

content = re.sub(r'components\.html\("""\n<script>\n.*?height=0, width=0\)', new_script, content, flags=re.DOTALL)

with open("app.py", "w") as f:
    f.write(content)
print("app.py updated")
