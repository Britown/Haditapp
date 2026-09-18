import re

with open("app.py", "r") as f:
    content = f.read()

old_hist = """                with st.expander(f"{doc.id} - Total: ${doc.to_dict().get('total', 0):,}"):
                    st.json(doc.to_dict())"""

new_hist = """                data = doc.to_dict()
                total = data.get('total_neto', 0)
                with st.expander(f"{doc.id} - Total: {format_clp(total)} CLP"):
                    st.json(data)"""

content = content.replace(old_hist, new_hist)

with open("app.py", "w") as f:
    f.write(content)
print("Historial fixed")
