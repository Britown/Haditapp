with open("app.py", "r") as f:
    lines = f.readlines()

# The first `with col_right:` is at line 322 (index 321)
# The second `with col_right:` is at line 523 (index 522)
# We need to keep the FIRST col_right block and delete the second one?
# Wait, NO!
# The `Ajustes Dinámicos` was moved to the END of `col_left`.
# So lines 322 to 522 is the FIRST `col_right` block!
# Lines 523 to end is the SECOND `col_right` block!
# Let's delete from 523 to end!
