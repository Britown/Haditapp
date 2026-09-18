with open("app.py", "r") as f:
    content = f.read()

content = content.replace('    with col_left:\n', '    col_left, col_right = st.columns([1, 1.2], gap="large")\n    with col_left:\n')

with open("app.py", "w") as f:
    f.write(content)
