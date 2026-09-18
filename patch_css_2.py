import re

with open("app.py", "r") as f:
    content = f.read()

old_css_start = "st.markdown(\"\"\""
old_css_end = "</style>\n\"\"\", unsafe_allow_html=True)"

start_idx = content.find(old_css_start)
end_idx = content.find(old_css_end, start_idx) + len(old_css_end)

new_css = """st.markdown(\"\"\"
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }
    
    /* Clean up top padding */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        max-width: 1100px !important;
    }
    
    /* Header and Title */
    h1 {
        font-weight: 700 !important;
        letter-spacing: -0.025em;
        color: #1D1D1F !important;
        text-align: center;
    }
    
    /* Hide default radio buttons and style as pills */
    div[data-testid="stRadio"] {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    div[data-testid="stRadio"] > div {
        display: inline-flex !important;
        flex-direction: row !important;
        background: #E8E8ED !important;
        border-radius: 9999px !important;
        padding: 4px !important;
        gap: 4px !important;
    }
    div[data-testid="stRadio"] label {
        padding: 8px 20px !important;
        border-radius: 9999px !important;
        background: transparent !important;
        color: #86868B !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        cursor: pointer;
        transition: all 0.2s ease;
        border: none !important;
    }
    /* Streamlit hides the radio input, we target the checked state via aria-checked */
    div[data-testid="stRadio"] label[data-checked="true"] {
        background: #FFFFFF !important;
        color: #1D1D1F !important;
        box-shadow: 0 2px 8px -1px rgba(0, 0, 0, 0.04) !important;
    }
    div[data-testid="stRadio"] label:hover:not([data-checked="true"]) {
        color: #1D1D1F !important;
    }
    div[data-testid="stRadio"] .st-emotion-cache-1n76uvr { /* Hide the circle */
        display: none !important;
    }
    
    /* Expander / Cards */
    section[data-testid="stExpander"], div[data-testid="stVerticalBlock"] > div.element-container > div > section {
        border: 1px solid rgba(0,0,0,0.07) !important;
        border-radius: 24px !important;
        background: #FFFFFF !important;
        box-shadow: 0 4px 24px -2px rgba(0,0,0,0.04) !important;
    }
    
    /* Primary Button */
    .stButton>button {
        background-color: #1D1D1F !important;
        color: #FFFFFF !important;
        border-radius: 16px !important;
        border: none !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.15s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #000000 !important;
        transform: scale(0.99);
    }
    
    /* Inputs */
    .stSelectbox>div>div, .stTextInput>div>div, .stNumberInput>div>div {
        border-radius: 12px !important;
        border: 1px solid rgba(0,0,0,0.07) !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
</style>
\"\"\", unsafe_allow_html=True)
"""

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_css.strip() + "\n" + content[end_idx:]
    with open("app.py", "w") as f:
        f.write(content)
    print("CSS updated for Apple style!")
else:
    print("Failed to find CSS block")
