import os

os.makedirs(".streamlit", exist_ok=True)
with open(".streamlit/config.toml", "w") as f:
    f.write("""[theme]
base="light"
primaryColor="#0071E3"
backgroundColor="#F5F5F7"
secondaryBackgroundColor="#FFFFFF"
textColor="#1D1D1F"
font="sans serif"
""")
