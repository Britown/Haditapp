with open("app.py", "r") as f:
    content = f.read()

# Extract CSS
css_start = content.find('st.markdown("""\n<style>')
css_end = content.find('""", unsafe_allow_html=True)', css_start) + len('""", unsafe_allow_html=True)')
css_block = content[css_start:css_end]

# Extract HTML definitions
html_start = content.find('config_json = """{')
html_end = content.find('components.html(top_html, height=260, scrolling=False)') + len('components.html(top_html, height=260, scrolling=False)')
html_block = content[html_start:html_end]

# Remove them from their original locations
content = content[:html_start] + content[html_end:]
content = content.replace(css_block, "")

# Insert them at the top, right after page radio button
radio_idx = content.find('st.markdown("<hr style=\'margin-top: 5px; margin-bottom: 20px;\'>", unsafe_allow_html=True)')
radio_idx += len('st.markdown("<hr style=\'margin-top: 5px; margin-bottom: 20px;\'>", unsafe_allow_html=True)')

new_top = f"\n\n{css_block}\n\n{html_block}\n\n"
content = content[:radio_idx] + new_top + content[radio_idx:]

with open("app.py", "w") as f:
    f.write(content)
