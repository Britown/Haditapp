import streamlit as st
import streamlit.components.v1 as components

html = """
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = { corePlugins: { preflight: false }, theme: { extend: { colors: { myblue: '#123456' } } } }
</script>
<div class="bg-myblue text-white p-10 rounded-xl text-3xl font-bold shadow-2xl">This is inside an iframe</div>
"""

components.html(html, height=200)
