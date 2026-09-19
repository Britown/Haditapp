import re

with open("sheets_exporter.py", "r") as f:
    content = f.read()

old_func_def = "def export_to_sheets(resultados_dict, user_email):"
new_func_def = "def export_to_sheets(resultados_dict, df_var, user_email):"
content = content.replace(old_func_def, new_func_def)

old_write_logic = """
        sheet = sh.sheet1
        
        # Prepare data headers and rows
        rows = [["Fecha de Exportación", "Ítem de Gasto", "Monto Detectado (CLP)"]]
        now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        for k, v in resultados_dict.items():
            if v > 0:
                rows.append([now_str, k, v])
                
        # Append rows
        sheet.append_rows(rows)
        
        # Format header
        sheet.format('A1:C1', {'textFormat': {'bold': True}})
        
        return sh.url
"""

new_write_logic = """
        # Sheet 1: Gastos Fijos
        sheet1 = sh.sheet1
        sheet1.update_title("Gastos Fijos")
        
        rows1 = [["Fecha de Exportación", "Ítem Fijo", "Monto Detectado (CLP)"]]
        now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        for k, v in resultados_dict.items():
            if v > 0:
                rows1.append([now_str, k, v])
                
        sheet1.append_rows(rows1)
        sheet1.format('A1:C1', {'textFormat': {'bold': True}})
        
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
content = content.replace(old_write_logic.strip(), new_write_logic.strip())

with open("sheets_exporter.py", "w") as f:
    f.write(content)
