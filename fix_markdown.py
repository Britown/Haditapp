import re

with open("app.py", "r") as f:
    content = f.read()

old_str = "st.markdown(out, unsafe_allow_html=True)"
new_str = "st.markdown(re.sub(r'^[ \\t]+', '', out, flags=re.MULTILINE), unsafe_allow_html=True)"

content = content.replace(old_str, new_str)

with open("app.py", "w") as f:
    f.write(content)
print("Fixed!")
