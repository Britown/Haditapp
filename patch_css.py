import re

with open("app.py", "r") as f:
    content = f.read()

# Replace the existing CSS block
old_css_start = "st.markdown(\"\"\""
old_css_end = "</style>\n\"\"\", unsafe_allow_html=True)"

start_idx = content.find(old_css_start)
end_idx = content.find(old_css_end, start_idx) + len(old_css_end)

new_css = """st.markdown(\"\"\"
<style>
    /* Font styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Clean up top padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px !important;
    }
    
    /* Minimalist Cards */
    section[data-testid="stExpander"] {
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
        background: #FFFFFF !important;
    }
    
    .bg-surface-container-lowest {
        border: 1px solid #F3F4F6 !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 20px -4px rgba(0,0,0,0.03) !important;
        background-color: #FFFFFF !important;
        padding: 32px !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #111827 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 500 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stButton>button:hover {
        background-color: #374151 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transform: translateY(-1px);
    }
    
    /* Text inputs and Selectboxes */
    .stSelectbox>div>div, .stTextInput>div>div, .stNumberInput>div>div {
        border-radius: 8px !important;
        border: 1px solid #E5E7EB !important;
        background-color: #FFFFFF !important;
    }
    
    /* Data Editor / Dataframes */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        border: 1px solid #F3F4F6;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    
    /* Headers */
    h1 {
        font-weight: 700 !important;
        letter-spacing: -0.025em;
        color: #111827 !important;
    }
    h2, h3 {
        font-weight: 600 !important;
        letter-spacing: -0.015em;
        color: #111827 !important;
    }
    
    /* Remove streamlit footer and menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
\"\"\", unsafe_allow_html=True)
"""

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_css.strip() + "\n" + content[end_idx:]
    with open("app.py", "w") as f:
        f.write(content)
    print("CSS injected!")
else:
    print("Failed to find CSS block")
