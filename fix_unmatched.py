import re

with open("processor.py", "r") as f:
    content = f.read()

# 1. Add UNMATCHED to is_usd_candidate
content = content.replace(
    'is_usd_candidate = cat in ["AMAZON PRIME", "HBO MAX", "YOUTUBE PREMIUM", "SPOTIFY DUO"]',
    'is_usd_candidate = cat in ["AMAZON PRIME", "HBO MAX", "YOUTUBE PREMIUM", "SPOTIFY DUO", "UNMATCHED"]'
)

# 2. Add time stripping before amounts regex
old_strip = """        line_for_amounts = re.sub(r'\\b\\d{1,2}\\.\\d{3}\\.\\d{3}-[\\dkK]\\b', '', line_for_amounts, flags=re.IGNORECASE)
        line_for_amounts = re.sub(r'\\b\\d{7,8}-[\\dkK]\\b', '', line_for_amounts, flags=re.IGNORECASE)"""

new_strip = """        line_for_amounts = re.sub(r'\\b\\d{1,2}\\.\\d{3}\\.\\d{3}-[\\dkK]\\b', '', line_for_amounts, flags=re.IGNORECASE)
        line_for_amounts = re.sub(r'\\b\\d{7,8}-[\\dkK]\\b', '', line_for_amounts, flags=re.IGNORECASE)
        # Eliminar horas para que no se confundan con montos pequeños en dolares
        line_for_amounts = re.sub(r'\\b\\d{1,2}:\\d{2}(?::\\d{2})?\\b', '', line_for_amounts)"""

content = content.replace(old_strip, new_strip)

# 3. Only process UNMATCHED if fecha != "N/A"
old_unmatched = """        if not cambio:
            best_val = get_best_amount(amounts, "UNMATCHED", fecha)"""

new_unmatched = """        if not cambio and fecha != "N/A":
            best_val = get_best_amount(amounts, "UNMATCHED", fecha)"""

content = content.replace(old_unmatched, new_unmatched)

with open("processor.py", "w") as f:
    f.write(content)
