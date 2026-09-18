import pandas as pd

def append_new_rules(edited_df):
    try:
        # Load existing rules
        df_rules = pd.read_csv("reglas_variables.csv")
        existing_matches = set(df_rules['match_text'].astype(str).str.upper())
        
        new_rules = []
        for _, row in edited_df.iterrows():
            desc = row['Descripción']
            cat = row['Categoría']
            resp = row['Responsable']
            
            # If the user classified it as something meaningful
            if cat not in ["Por Revisar", "Sin Categorizar"] and resp != "Por Revisar":
                if desc.upper() not in existing_matches:
                    new_rules.append({
                        "match_text": desc,
                        "category": cat,
                        "owner": resp,
                        "priority": 1,
                        "notes": "Agregado automáticamente por entrenamiento"
                    })
                    existing_matches.add(desc.upper())
                    
        if new_rules:
            new_df = pd.DataFrame(new_rules)
            df_rules = pd.concat([df_rules, new_df], ignore_index=True)
            df_rules.to_csv("reglas_variables.csv", index=False)
            return len(new_rules)
    except Exception as e:
        print("Error appending rules:", e)
    return 0
