import re

with open("app.py", "r") as f:
    content = f.read()

# I need to find where I do:
#        if "_Original" in edited_df.columns:
#            edited_df = edited_df.drop(columns=["_Original"])
# And change it to keep it in edited_df, but create edited_df_db = edited_df.drop...

bad_drop = """
        if "_Original" in edited_df.columns:
            edited_df = edited_df.drop(columns=["_Original"])
"""
good_drop = """
        # Keep _Original in edited_df for training logic
        edited_df_clean = edited_df.drop(columns=["_Original"]) if "_Original" in edited_df.columns else edited_df
"""
content = content.replace(bad_drop, good_drop)

# Then replace database.save_gastos_variables(db, month_to_save, edited_df)
# with database.save_gastos_variables(db, month_to_save, edited_df_clean)
content = content.replace("database.save_gastos_variables(db, month_to_save, edited_df)", "database.save_gastos_variables(db, month_to_save, edited_df_clean)")

with open("app.py", "w") as f:
    f.write(content)
print("Fixed!")
