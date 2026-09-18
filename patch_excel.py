import re

with open("app.py", "r") as f:
    content = f.read()

bad_excel = """
                # 3 sheets exactly as requested
                edited_identificados.to_excel(writer, index=False, sheet_name="Gastos")
                edited_ingresos.to_excel(writer, index=False, sheet_name="Abonos")
                edited_no_identificados.to_excel(writer, index=False, sheet_name="Gastos no identificados")
"""
good_excel = """
                # 3 sheets exactly as requested
                def drop_orig(df):
                    return df.drop(columns=["_Original"]) if "_Original" in df.columns else df
                    
                drop_orig(edited_identificados).to_excel(writer, index=False, sheet_name="Gastos")
                drop_orig(edited_ingresos).to_excel(writer, index=False, sheet_name="Abonos")
                drop_orig(edited_no_identificados).to_excel(writer, index=False, sheet_name="Gastos no identificados")
"""
content = content.replace(bad_excel, good_excel)

with open("app.py", "w") as f:
    f.write(content)
print("Excel fixed!")
