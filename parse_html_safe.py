import re

with open("stitch_ui/code.html", "r") as f:
    html = f.read()

# Extract Tailwind config
match = re.search(r'tailwind\.config = (\{.*?\});', html, re.DOTALL)
config_json = match.group(1) if match else "{}"

# Extract Header + Hero block
# It starts at <header class="fixed top-0 and ends after the Date & Settlement Capsule.
header_match = re.search(r'(<header class="fixed top-0.*?</header>)', html, re.DOTALL)
header_html = header_match.group(1)

# The main wrapper starts at <main class="w-full pt-16
# We want the hero which is <header class="flex flex-col lg:flex-row lg:items-end justify-between gap-space-md">
hero_match = re.search(r'(<header class="flex flex-col lg:flex-row.*?</header>)', html, re.DOTALL)
hero_html = hero_match.group(1)

# Write to a dump file to inspect
with open("dump.html", "w") as f:
    f.write("<!-- HEADER -->\n" + header_html + "\n<!-- HERO -->\n" + hero_html)

print("Parsed.")

right_match = re.search(r'(<!-- RIGHT COLUMN:.*?)<!-- Antigravity Direct Status Pill Container -->', html, re.DOTALL)
if not right_match:
    right_match = re.search(r'(<!-- RIGHT COLUMN:.*?)</main>', html, re.DOTALL)
right_html = right_match.group(1) if right_match else ""

with open("dump.html", "a") as f:
    f.write("\n<!-- RIGHT -->\n" + right_html[:200] + "...")
