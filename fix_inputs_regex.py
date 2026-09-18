import re
with open("app.py", "r") as f:
    content = f.read()

# Replace any st.markdown('<div class="ui-card">...</div>', unsafe_allow_html=True)
# where the string spans multiple lines but is wrapped in single quotes.
content = re.sub(r"st\.markdown\('(<div class=\"ui-card\">.*?)', unsafe_allow_html=True\)", 
                 r"st.markdown('''\1''', unsafe_allow_html=True)", 
                 content, flags=re.DOTALL)

with open("app.py", "w") as f:
    f.write(content)
