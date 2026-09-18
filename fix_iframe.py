with open("app.py", "r") as f:
    content = f.read()

content = content.replace("components.html(final_right, height=880, scrolling=False)", "components.html(final_right, height=1400, scrolling=True)")

with open("app.py", "w") as f:
    f.write(content)
