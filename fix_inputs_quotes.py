with open("app.py", "r") as f:
    content = f.read()

# Fix the multiline strings in st.markdown
content = content.replace("st.markdown('<div class=\"ui-card\">\\n", "st.markdown('''<div class=\"ui-card\">\\n")
content = content.replace("automática.</div>', unsafe_allow_html=True)", "automática.</div>''', unsafe_allow_html=True)")
content = content.replace("lectura.</div>', unsafe_allow_html=True)", "lectura.</div>''', unsafe_allow_html=True)")

with open("app.py", "w") as f:
    f.write(content)
