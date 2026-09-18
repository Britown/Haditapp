import re

with open("app.py", "r") as f:
    content = f.read()

# Remove the opening and closing <section> tags from the left column
content = content.replace("st.markdown('<section style=\"background: #FFFFFF; border-radius: 24px; padding: 32px; border: 1px solid rgba(0,0,0,0.07); box-shadow: 0 4px 24px -2px rgba(0,0,0,0.04); margin-bottom: 24px;\">', unsafe_allow_html=True)", "")
content = content.replace("st.markdown('</section>', unsafe_allow_html=True)", "")

with open("app.py", "w") as f:
    f.write(content)
print("Removed empty section tags")
