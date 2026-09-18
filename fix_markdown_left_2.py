import re

with open("app.py", "r") as f:
    content = f.read()

# Replace all st.markdown(r""" ... """, unsafe_allow_html=True) with a version that dedents
def replacer(match):
    inner = match.group(1)
    return "st.markdown(re.sub(r'^[ \\t]+', '', r\"\"\"" + inner + "\"\"\", flags=re.MULTILINE), unsafe_allow_html=True)"

content = re.sub(r'st\.markdown\(r\"\"\"(.*?)\"\"\",\s*unsafe_allow_html=True\)', replacer, content, flags=re.DOTALL)

with open("app.py", "w") as f:
    f.write(content)
print("Fixed all remaining multi-line st.markdown calls!")
