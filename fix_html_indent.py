import re
with open("app.py", "r") as f:
    content = f.read()

# Add import re at the top if missing
if "import re" not in content:
    content = "import re\n" + content

# Replace `st.markdown(out, unsafe_allow_html=True)` with `st.markdown(re.sub(r'^\s+', '', out, flags=re.MULTILINE), unsafe_allow_html=True)`
old_md = "st.markdown(out, unsafe_allow_html=True)"
new_md = "st.markdown(re.sub(r'^\\\\s+', '', out, flags=re.MULTILINE), unsafe_allow_html=True)"

if old_md in content:
    content = content.replace(old_md, new_md)
    with open("app.py", "w") as f:
        f.write(content)
