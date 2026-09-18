with open("app.py", "r") as f:
    content = f.read()

old_style = """            st.dataframe(
                df.style.format({
                    "Total Fijos": "${:,.0f}",
                    "Cuota Papá": "${:,.0f}",
                    "Deuda Mamá": "${:,.0f}"
                }).background_gradient(cmap="Blues", subset=["Total Fijos"]),
                use_container_width=True
            )"""

new_style = """            st.dataframe(
                df.style.format({
                    "Total Fijos": "${:,.0f}",
                    "Cuota Papá": "${:,.0f}",
                    "Deuda Mamá": "${:,.0f}"
                }),
                use_container_width=True
            )"""

content = content.replace(old_style, new_style)

with open("app.py", "w") as f:
    f.write(content)
