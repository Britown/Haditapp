with open("sheets_exporter.py", "r") as f:
    content = f.read()

old_logic = """
        if not sheet_url:
            st.error("Por favor, ingresa una URL válida de Google Sheets.")
            return False
            
        sheet = client.open_by_url(sheet_url).sheet1
        
        # Prepare data: Date, Name, Amount
        now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        rows = []
        for k, v in resultados_dict.items():
            if v > 0:
                rows.append([now_str, k, v])
                
        # Append rows
        sheet.append_rows(rows)
        return True
"""

new_logic = """
        if not sheet_url or "@" not in sheet_url:
            st.error("Por favor, ingresa un correo electrónico válido.")
            return False
            
        user_email = sheet_url.strip()
        
        # Create a new spreadsheet
        title = f"Haditapp - Gastos {datetime.now().strftime('%d %b %Y %H:%M')}"
        sh = client.create(title)
        
        # Share it with the user so they can see it in their Google Drive
        sh.share(user_email, perm_type='user', role='writer')
        
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

content = content.replace("def export_to_sheets(resultados_dict, sheet_url):", "def export_to_sheets(resultados_dict, user_email):")
content = content.replace(old_logic.strip(), new_logic.strip())

with open("sheets_exporter.py", "w") as f:
    f.write(content)

