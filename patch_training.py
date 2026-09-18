import re

with open("app.py", "r") as f:
    content = f.read()

# 1. Add _Original column to the splitted DataFrames
split_logic_old = """
        # Split DataFrames
        df_ingresos = df_vars[df_vars["Categoría"] == "Ingresos"].reset_index(drop=True)
        df_no_identificados = df_vars[df_vars["Categoría"] == "Por Revisar"].reset_index(drop=True)
        df_identificados = df_vars[(df_vars["Categoría"] != "Ingresos") & (df_vars["Categoría"] != "Por Revisar")].reset_index(drop=True)
"""
split_logic_new = """
        # Split DataFrames
        df_vars["_Original"] = df_vars["Descripción"]
        df_ingresos = df_vars[df_vars["Categoría"] == "Ingresos"].reset_index(drop=True)
        df_no_identificados = df_vars[df_vars["Categoría"] == "Por Revisar"].reset_index(drop=True)
        df_identificados = df_vars[(df_vars["Categoría"] != "Ingresos") & (df_vars["Categoría"] != "Por Revisar")].reset_index(drop=True)
"""
content = content.replace(split_logic_old, split_logic_new)

# 2. Hide _Original column
col_config_old = """
            "Descripción": st.column_config.TextColumn(
                "Descripción",
                width="large"
            )
        }
"""
col_config_new = """
            "Descripción": st.column_config.TextColumn(
                "Descripción",
                width="large"
            ),
            "_Original": None
        }
"""
content = content.replace(col_config_old, col_config_new)

# 3. Update the training logic to use _Original for match_text, and Descripción for clean_name
train_logic_old = """
                        for _, row in edited_df.iterrows():
                            desc, cat, resp = row['Descripción'], row['Categoría'], row['Responsable']
                            if cat not in ["Por Revisar", "Sin Categorizar"] and resp != "Por Revisar":
                                if desc.upper() not in existing:
                                    new_rules.append({
                                        "match_text": desc, "category": cat, "owner": resp, 
                                        "priority": 1, "notes": "Entrenamiento manual", "clean_name": desc
                                    })
                                    existing.add(desc.upper())
"""
train_logic_new = """
                        for _, row in edited_df.iterrows():
                            desc, cat, resp = row['Descripción'], row['Categoría'], row['Responsable']
                            orig = row.get('_Original', desc)
                            if cat not in ["Por Revisar", "Sin Categorizar"] and resp != "Por Revisar":
                                if orig.upper() not in existing:
                                    # If user changed description, save it as clean_name
                                    clean_val = desc if desc != orig else ""
                                    new_rules.append({
                                        "match_text": orig, "category": cat, "owner": resp, 
                                        "priority": 1, "notes": "Entrenamiento manual", "clean_name": clean_val
                                    })
                                    existing.add(orig.upper())
"""
content = content.replace(train_logic_old, train_logic_new)

# Drop _Original before saving to database and excel
drop_logic_old = """
        # Combine back into a single dataframe for saving
        import pandas as pd
        edited_df = pd.concat([edited_no_identificados, edited_identificados, edited_ingresos], ignore_index=True)
"""
drop_logic_new = """
        # Combine back into a single dataframe for saving
        import pandas as pd
        edited_df = pd.concat([edited_no_identificados, edited_identificados, edited_ingresos], ignore_index=True)
        if "_Original" in edited_df.columns:
            edited_df = edited_df.drop(columns=["_Original"])
"""
content = content.replace(drop_logic_old, drop_logic_new)

with open("app.py", "w") as f:
    f.write(content)
print("Patched app.py to support changing descriptions safely!")
