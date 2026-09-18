from bs4 import BeautifulSoup

with open("stitch_ui/code.html", "r") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

header = soup.find("header")
print("--- HEADER ---")
print(str(header)[:200])

hero = soup.find("header", class_=lambda x: x and "flex-col lg:flex-row" in x)
print("\n--- HERO ---")
print(str(hero)[:200])

ajustes = soup.find("section", class_=lambda x: x and "bg-surface-container-lowest" in x)
print("\n--- AJUSTES HEADER ---")
print(str(ajustes.find("div", class_="flex items-start justify-between")))

ingesta = soup.find_all("section")[1]
print("\n--- INGESTA HEADER ---")
print(str(ingesta.find("div", class_="flex items-start justify-between")))

right_col = soup.find("div", class_=lambda x: x and "lg:col-span-7" in x)
print("\n--- RIGHT COL ---")
print(str(right_col)[:200])
