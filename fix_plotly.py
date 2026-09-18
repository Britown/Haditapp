with open("app.py", "r") as f:
    content = f.read()

old_plotly = """                    with c2:
                        import plotly.express as px
                        fig = px.pie(df_desglose, values='Monto', names='Ítem', hole=0.4)
                        fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
                        st.plotly_chart(fig, use_container_width=True)"""

new_plotly = """                    with c2:
                        st.bar_chart(df_desglose.set_index("Ítem")["Monto"])"""

content = content.replace(old_plotly, new_plotly)

with open("app.py", "w") as f:
    f.write(content)
