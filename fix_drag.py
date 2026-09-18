with open("app.py", "r") as f:
    content = f.read()

old_drag = """        tab1, tab2 = st.tabs(["Arrastrar Archivos", "Pegar Texto"])
        with tab1:
            uploaded_files = st.file_uploader("Arrastra tu cartola bancaria", accept_multiple_files=True, label_visibility="collapsed")
        with tab2:
            pasted_text = st.text_area("Pega aquí la cartola", height=120, label_visibility="collapsed")"""

new_drag = """        st.markdown("<span class='font-label-sm uppercase tracking-wider text-on-surface-variant' style='font-size:11px; font-weight:600; color:#4c4546;'>Cartola PDF</span>", unsafe_allow_html=True)
        uploaded_files = st.file_uploader("Arrastra tu cartola bancaria", accept_multiple_files=True, label_visibility="collapsed")
        
        st.markdown("<span class='font-label-sm uppercase tracking-wider text-on-surface-variant' style='font-size:11px; font-weight:600; color:#4c4546; margin-top:10px; display:inline-block;'>O pega el texto aquí</span>", unsafe_allow_html=True)
        pasted_text = st.text_area("Pega aquí la cartola", height=120, label_visibility="collapsed")"""

if old_drag in content:
    content = content.replace(old_drag, new_drag)
    with open("app.py", "w") as f:
        f.write(content)
