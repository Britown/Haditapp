with open("app.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    if "st.session_state.unmatched = unmatched" in line:
        new_lines.append(line.replace("st.session_state.unmatched = unmatched", "st.session_state.current_month_str = month_str"))

with open("app.py", "w") as f:
    f.writelines(new_lines)
