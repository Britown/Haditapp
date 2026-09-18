import streamlit as st
import streamlit.components.v1 as components

st.markdown('<div class="bg-blue-500 text-white p-10 rounded-xl text-3xl font-bold shadow-2xl">This is Tailwind injected into Streamlit!</div>', unsafe_allow_html=True)

components.html("""
<script>
    if (!window.parent.document.getElementById('tailwind-script')) {
        const tailwind = window.parent.document.createElement('script');
        tailwind.id = 'tailwind-script';
        tailwind.src = 'https://cdn.tailwindcss.com';
        window.parent.document.head.appendChild(tailwind);
    }
</script>
""", height=0, width=0)
