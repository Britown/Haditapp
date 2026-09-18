with open("app.py", "r") as f:
    content = f.read()

import re
old_logic = """now = datetime.datetime.now()
curr_m_idx = now.month - 1
curr_y_idx = [2024, 2025, 2026, 2027].index(now.year) if now.year in [2024, 2025, 2026, 2027] else 2"""

new_logic = """now = datetime.datetime.now()
prev_month = now.month - 1
target_year = now.year

if prev_month == 0:
    prev_month = 12
    target_year -= 1

curr_m_idx = prev_month - 1
curr_y_idx = [2024, 2025, 2026, 2027].index(target_year) if target_year in [2024, 2025, 2026, 2027] else 2"""

content = content.replace(old_logic, new_logic)

with open("app.py", "w") as f:
    f.write(content)
