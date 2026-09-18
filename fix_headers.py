with open("app.py", "r") as f:
    content = f.read()

# We want to remove the block from `st.markdown(r"""<header class="fixed top-0` down to right before `with col_left:`
start_idx = content.find('    st.markdown(r"""<header class="fixed top-0')
end_idx = content.find('    with col_left:')

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + content[end_idx:]
    with open("app.py", "w") as f:
        f.write(content)
