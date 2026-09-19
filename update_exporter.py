with open("sheets_exporter.py", "r") as f:
    content = f.read()

# Replace the create logic
old_logic = """
        if not user_email or "@" not in user_email:
            st.error("Por favor, ingresa un correo electrónico válido.")
            return False
            
        user_email = user_email.strip()
        
        # Create a new spreadsheet
        title = f"Haditapp - Gastos {datetime.now().strftime('%d %b %Y %H:%M')}"
        sh = client.create(title)
        
        # Share it with the user so they can see it in their Google Drive
        sh.share(user_email, perm_type='user', role='writer')
        
        # Sheet 1: Gastos Fijos
        sheet1 = sh.sheet1
        sheet1.update_title("Gastos Fijos")
"""

new_logic = """
        master_url = st.secrets.get("gcp_service_account", {}).get("master_sheet_url")
        if not master_url:
            st.error("No se encontró 'master_sheet_url' en los secretos.")
            return False
            
        # Open existing spreadsheet
        sh = client.open_by_url(master_url)
        
        suffix = f" {datetime.now().strftime('%d/%m %H:%M')}"
        
        # Helper to create tab safely
        def create_tab(name, cols="6"):
            # Truncate if too long, gspread limits to 100 chars but usually fine
            full_name = f"{name}{suffix}"
            try:
                # If for some reason it exists, add seconds
                return sh.add_worksheet(title=full_name, rows="100", cols=cols)
            except:
                return sh.add_worksheet(title=f"{full_name} {datetime.now().strftime('%S')}", rows="100", cols=cols)

        # Create new tabs for this export
        sheet1 = create_tab("Fijos")
"""
content = content.replace(old_logic.strip(), new_logic.strip())

# The inner _write_df_to_tab also uses sh.add_worksheet
old_inner = """
        def _write_df_to_tab(tab_title, df):
            sheet = sh.add_worksheet(title=tab_title, rows="100", cols="6")
"""
new_inner = """
        def _write_df_to_tab(tab_title, df):
            sheet = create_tab(tab_title)
"""
content = content.replace(old_inner.strip(), new_inner.strip())

# Change signature from export_to_sheets(..., user_email) to no user_email
content = content.replace(
    "def export_to_sheets(resultados_dict, df_identificados, df_no_identificados, df_ingresos, user_email):",
    "def export_to_sheets(resultados_dict, df_identificados, df_no_identificados, df_ingresos):"
)

with open("sheets_exporter.py", "w") as f:
    f.write(content)
