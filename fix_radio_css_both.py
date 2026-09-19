import re
with open("app.py", "r") as f:
    content = f.read()

# I will just duplicate the CSS selectors so it targets BOTH stRadio and stRadioGroup
# and data-checked and data-selected.

# We will just write a new python script to replace the CSS to support BOTH forms.
