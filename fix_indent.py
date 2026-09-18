with open("app.py", "r") as f:
    content = f.read()

bad = """st.markdown("</div>", unsafe_allow_html=True)
    st.button("Procesar Gastos Fijos (Cmd + Enter)", on_click=do_process)"""
good = """    st.markdown("</div>", unsafe_allow_html=True)
    st.button("Procesar Gastos Fijos (Cmd + Enter)", on_click=do_process)"""

content = content.replace(bad, good)

with open("app.py", "w") as f:
    f.write(content)
