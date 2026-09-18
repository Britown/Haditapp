import re

with open("app.py", "r") as f:
    content = f.read()

# Add import
content = content.replace("from processor import extract_all_text, process_data", "from processor import extract_all_text, process_data\nfrom variables_processor import process_unmatched_to_df")

old_vars = """if page == "Gastos Variables":
    st.title("Gastos Variables (En Construcción 🚧)")
    st.info("Aquí cargaremos las cartolas para analizar supermercado, farmacia y otros gastos no fijos, descartando automáticamente los que ya fueron procesados en la conciliación fija.")
    st.stop()"""

new_vars = """if page == "Gastos Variables":
    st.title("Clasificador de Gastos Variables 🔍")
    st.markdown("Aquí se listan todos los gastos de la cartola que **no fueron procesados en la Conciliación Fija**. El sistema intentará clasificarlos automáticamente usando tus reglas (Jumbo, Farmacias, Wisecity, etc).")
    
    if "unmatched" not in st.session_state or not st.session_state.unmatched:
        st.warning("No hay gastos variables en la memoria. Primero ve a 'Conciliación Fija', sube una cartola y procésala.")
        st.stop()
        
    df_vars = process_unmatched_to_df(st.session_state.unmatched)
    
    if df_vars.empty:
        st.info("Todos los gastos de la cartola eran fijos. ¡No hay gastos variables que procesar!")
        st.stop()
        
    st.markdown("### Revisa y Corrige")
    st.markdown("La IA/Reglas pre-clasificó los gastos. Puedes editar la Categoría y el Responsable haciendo doble clic en la celda.")
    
    # Categorias permitidas
    categorias = ["Supermercado", "Salud", "Combustible", "Suscripciones", "Entretenimiento", "Compras hogar", "Restaurant-café", "Delivery", "Ingresos", "Mercado Pago", "No Identificado", "Sin Categorizar"]
    responsables = ["Compartido", "Personal", "Confirmar"]
    
    edited_df = st.data_editor(
        df_vars,
        column_config={
            "Categoría": st.column_config.SelectboxColumn("Categoría", options=categorias, required=True),
            "Responsable": st.column_config.SelectboxColumn("Responsable (Compartido/Personal)", options=responsables, required=True),
            "Monto": st.column_config.NumberColumn("Monto ($)", format="$ %d")
        },
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic"
    )
    
    # Calcular resumen
    df_compartido = edited_df[edited_df["Responsable"] == "Compartido"]
    total_compartido = df_compartido["Monto"].sum()
    
    st.markdown(f"### 💰 Total Compartido Variable: $ {int(total_compartido):,}".replace(",", "."))
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Guardar Gastos Variables", type="primary", use_container_width=True):
            st.success("¡Gastos guardados! (Conexión a Firebase para variables pendiente de habilitar)")
            
    st.stop()"""

content = content.replace(old_vars, new_vars)

with open("app.py", "w") as f:
    f.write(content)
