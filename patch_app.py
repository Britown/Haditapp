import re

with open("app.py", "r") as f:
    content = f.read()

# 1. Change SelectboxColumn to TextColumn for Categoría
target_select = """            "Categoría": st.column_config.SelectboxColumn(
                "Categoría",
                help="Categoría del gasto",
                width="medium",
                options=["Supermercado", "Farmacia", "Gustitos", "Delivery", "Salud", "Combustible", "Suscripciones", "Entretenimiento", "Seguros", "Babysit", "Librería", "Minimarket", "Pago cuota casa", "Pago deuda Omita", "Gastos Bancarios", "Pago Tarjeta", "Mercadería", "Compras hogar", "Restaurant-café", "Ingresos", "Mercado Pago", "Por Revisar"]
            ),"""
replacement_select = """            "Categoría": st.column_config.TextColumn(
                "Categoría (editable)",
                help="Escribe la categoría que desees",
                width="medium"
            ),"""
content = content.replace(target_select, replacement_select)

# 2. Add Totals to the UI
# Find editor_no_id
target_no_id = """        edited_no_identificados = st.data_editor(
            df_no_identificados,
            column_config=col_config,
            hide_index=True,
            use_container_width=True,
            key="editor_no_id"
        )"""
replacement_no_id = target_no_id + """
        if not edited_no_identificados.empty:
            st.markdown(f"<p style='text-align:right; font-weight:600; font-size:15px; color:#1D1D1F;'>Total Pendientes: $ {format_clp(edited_no_identificados['Monto'].sum())}</p>", unsafe_allow_html=True)"""
content = content.replace(target_no_id, replacement_no_id)

# Find editor_id
target_id = """        edited_identificados = st.data_editor(
            df_identificados,
            column_config=col_config,
            hide_index=True,
            use_container_width=True,
            key="editor_id"
        )"""
replacement_id = target_id + """
        if not edited_identificados.empty:
            st.markdown(f"<p style='text-align:right; font-weight:600; font-size:15px; color:#1D1D1F;'>Total Identificados: $ {format_clp(edited_identificados['Monto'].sum())}</p>", unsafe_allow_html=True)"""
content = content.replace(target_id, replacement_id)

# Find editor_ingresos
target_ing = """        edited_ingresos = st.data_editor(
            df_ingresos,
            column_config=col_config,
            hide_index=True,
            use_container_width=True,
            key="editor_ingresos"
        )"""
replacement_ing = target_ing + """
        if not edited_ingresos.empty:
            st.markdown(f"<p style='text-align:right; font-weight:600; font-size:15px; color:#1D1D1F;'>Total Ingresos: $ {format_clp(edited_ingresos['Monto'].sum())}</p>", unsafe_allow_html=True)"""
content = content.replace(target_ing, replacement_ing)

# 3. Add st.rerun() after training
target_toast = 'st.toast(f"🧠 Se han aprendido {len(new_rules)} nuevas reglas.")'
replacement_toast = target_toast + '\n                        st.rerun()'
content = content.replace(target_toast, replacement_toast)

with open("app.py", "w") as f:
    f.write(content)
