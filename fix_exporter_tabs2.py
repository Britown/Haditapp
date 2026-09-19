import re

with open("sheets_exporter.py", "r") as f:
    content = f.read()

# Change the function signature
content = content.replace(
    "def export_to_sheets(resultados_dict, df_var, user_email):",
    "def export_to_sheets(resultados_dict, df_identificados, df_no_identificados, df_ingresos, user_email):"
)

old_write_logic = """
        # Sheet 2: Gastos Variables
        sheet2 = sh.add_worksheet(title="Gastos Variables", rows="100", cols="6")
        rows2 = [["Fecha", "Descripción", "Categoría", "Responsable", "Monto (CLP)"]]
        
        if df_var is not None and not df_var.empty:
            for _, row in df_var.iterrows():
                rows2.append([
                    str(row.get('Fecha', '')), 
                    str(row.get('Descripción', '')), 
                    str(row.get('Categoría', '')), 
                    str(row.get('Responsable', '')), 
                    int(row.get('Monto', 0))
                ])
                
        sheet2.append_rows(rows2)
        sheet2.format('A1:E1', {'textFormat': {'bold': True}})
        
        return sh.url
"""

new_write_logic = """
        def _write_df_to_tab(tab_title, df):
            sheet = sh.add_worksheet(title=tab_title, rows="100", cols="6")
            rows = [["Fecha", "Descripción", "Categoría", "Responsable", "Monto (CLP)"]]
            if df is not None and not df.empty:
                for _, row in df.iterrows():
                    rows.append([
                        str(row.get('Fecha', '')), 
                        str(row.get('Descripción', '')), 
                        str(row.get('Categoría', '')), 
                        str(row.get('Responsable', '')), 
                        int(row.get('Monto', 0))
                    ])
            sheet.append_rows(rows)
            sheet.format('A1:E1', {'textFormat': {'bold': True}})

        # Pestañas adicionales
        _write_df_to_tab("Identificados", df_identificados)
        _write_df_to_tab("Por Revisar", df_no_identificados)
        _write_df_to_tab("Ingresos", df_ingresos)
        
        return sh.url
"""

content = content.replace(old_write_logic.strip(), new_write_logic.strip())

with open("sheets_exporter.py", "w") as f:
    f.write(content)
