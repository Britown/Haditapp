import re

with open("app.py", "r") as f:
    content = f.read()

# Define the new Gastos Variables block
new_block = """
elif page == "Gastos Variables":
    st.header("Gastos Variables, Abonos y Entrenamiento")
    if 'unmatched' in st.session_state and st.session_state.unmatched:
        with st.spinner("Clasificando con IA y Reglas..."):
            df_vars = process_unmatched_to_df(st.session_state.unmatched)
            
        # Split DataFrames
        df_ingresos = df_vars[df_vars["Categoría"] == "Ingresos"].reset_index(drop=True)
        df_no_identificados = df_vars[df_vars["Categoría"] == "Por Revisar"].reset_index(drop=True)
        df_identificados = df_vars[(df_vars["Categoría"] != "Ingresos") & (df_vars["Categoría"] != "Por Revisar")].reset_index(drop=True)
        
        col_config = {
            "Categoría": st.column_config.SelectboxColumn(
                "Categoría",
                help="Categoría del gasto",
                width="medium",
                options=["Supermercado", "Farmacia", "Gustitos", "Delivery", "Salud", "Combustible", "Suscripciones", "Entretenimiento", "Seguros", "Babysit", "Librería", "Minimarket", "Pago cuota casa", "Pago deuda Omita", "Gastos Bancarios", "Pago Tarjeta", "Mercadería", "Compras hogar", "Restaurant-café", "Ingresos", "Mercado Pago", "Por Revisar"]
            ),
            "Responsable": st.column_config.SelectboxColumn(
                "Responsabilidad",
                help="Quién asume este gasto",
                width="small",
                options=["Compartido", "Personal", "Por Revisar"]
            ),
            "Monto": st.column_config.NumberColumn(
                "Monto ($)",
                help="Valor de la transacción",
                format="$ %d"
            ),
            "Descripción": st.column_config.TextColumn(
                "Descripción",
                width="large"
            )
        }
        
        st.subheader("⚠️ Gastos Pendientes por Entrenar")
        st.markdown("Clasifica estos gastos. El sistema aprenderá automáticamente para la próxima vez.")
        edited_no_identificados = st.data_editor(
            df_no_identificados,
            column_config=col_config,
            hide_index=True,
            use_container_width=True,
            key="editor_no_id"
        )
        
        st.subheader("✅ Gastos Identificados")
        st.markdown("Gastos que el sistema ya reconoce. Puedes corregirlos si se equivocó.")
        edited_identificados = st.data_editor(
            df_identificados,
            column_config=col_config,
            hide_index=True,
            use_container_width=True,
            key="editor_id"
        )
        
        st.subheader("💰 Abonos / Ingresos")
        st.markdown("Transferencias recibidas o abonos detectados.")
        edited_ingresos = st.data_editor(
            df_ingresos,
            column_config=col_config,
            hide_index=True,
            use_container_width=True,
            key="editor_ingresos"
        )
        
        # Combine back into a single dataframe for saving
        import pandas as pd
        edited_df = pd.concat([edited_no_identificados, edited_identificados, edited_ingresos], ignore_index=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Guardar y Entrenar Sistema"):
                month_to_save = st.session_state.get('current_month_str', 'Desconocido')
                db = database.init_db()
                if db:
                    database.save_gastos_variables(db, month_to_save, edited_df)
                    
                    # Entrenamiento automático
                    try:
                        df_rules = pd.read_csv("reglas_variables.csv")
                        existing = set(df_rules['match_text'].astype(str).str.upper())
                        new_rules = []
                        for _, row in edited_df.iterrows():
                            desc, cat, resp = row['Descripción'], row['Categoría'], row['Responsable']
                            if cat not in ["Por Revisar", "Sin Categorizar"] and resp != "Por Revisar":
                                if desc.upper() not in existing:
                                    new_rules.append({
                                        "match_text": desc, "category": cat, "owner": resp, 
                                        "priority": 1, "notes": "Entrenamiento manual", "clean_name": desc
                                    })
                                    existing.add(desc.upper())
                        if new_rules:
                            pd.concat([df_rules, pd.DataFrame(new_rules)], ignore_index=True).to_csv("reglas_variables.csv", index=False)
                            st.toast(f"🧠 Se han aprendido {len(new_rules)} nuevas reglas.")
                    except Exception as e:
                        print("Error guardando reglas:", e)
                        
                    st.success(f"¡Gastos Variables de {month_to_save} guardados en Firebase!")

        with col2:
            import io
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                # 3 sheets exactly as requested
                edited_identificados.to_excel(writer, index=False, sheet_name="Gastos")
                edited_ingresos.to_excel(writer, index=False, sheet_name="Abonos")
                edited_no_identificados.to_excel(writer, index=False, sheet_name="Gastos no identificados")
                
            st.download_button(
                label="📊 Exportar a Excel",
                data=excel_buffer.getvalue(),
                file_name=f"Gastos_Variables_{st.session_state.get('current_month_str', 'Mes')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    else:
        st.info("No hay gastos variables para mostrar. Primero procesa una cartola en 'Conciliación Fija'.")
"""

start_idx = content.find('elif page == "Gastos Variables":')
if start_idx != -1:
    end_idx = content.find('else:', content.find('st.info("No hay gastos variables para mostrar', start_idx))
    if end_idx != -1:
        end_idx = content.find('\n', end_idx) # go to end of line
        end_idx = content.find('\n', content.find('st.info("No hay', start_idx)) + 1
        # Re-find the exact block
        match = re.search(r'elif page == "Gastos Variables":.*?(?=st\.info\("No hay gastos variables para mostrar.*?\)[\n\r]+)', content, re.DOTALL)
        if match:
            # We replace exactly the block
            full_match = match.group(0) + 'st.info("No hay gastos variables para mostrar. Primero procesa una cartola en \'Conciliación Fija\'.")\n'
            content = content.replace(full_match, new_block)
            with open("app.py", "w") as f:
                f.write(content)
            print("Successfully patched app.py!")
