import re

with open("app.py", "r") as f:
    content = f.read()

# Make the Historial blocks responsive
content = content.replace(
    '<div style="display: flex; gap: 16px; margin-bottom: 24px; padding: 16px; background: #FAFAFC; border-radius: 16px; border: 1px solid rgba(0,0,0,0.05);">',
    '<div style="display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 24px; padding: 16px; background: #FAFAFC; border-radius: 16px; border: 1px solid rgba(0,0,0,0.05);">'
)

content = content.replace(
    '<div style="display: flex; align-items: center; gap: 16px;">',
    '<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 16px;">'
)

# Fix the main dashboard blocks as well (Gastos Fijos)
content = content.replace(
    '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">',
    '<div style="display: flex; flex-wrap: wrap; gap: 16px;">\n                            <!-- Replaced grid with flex for mobile responsiveness -->'
)

# For the flex items that were in grid, we add min-width
content = content.replace(
    '<div style="background: rgba(0,113,227,0.05); border: 1px solid rgba(0,113,227,0.15); padding: 16px; border-radius: 16px;">',
    '<div style="flex: 1; min-width: 200px; background: rgba(0,113,227,0.05); border: 1px solid rgba(0,113,227,0.15); padding: 16px; border-radius: 16px;">'
)
content = content.replace(
    '<div style="background: rgba(124,58,237,0.05); border: 1px solid rgba(124,58,237,0.15); padding: 16px; border-radius: 16px;">',
    '<div style="flex: 1; min-width: 200px; background: rgba(124,58,237,0.05); border: 1px solid rgba(124,58,237,0.15); padding: 16px; border-radius: 16px;">'
)

with open("app.py", "w") as f:
    f.write(content)
print("Responsive fixed")
