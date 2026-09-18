import sys
import streamlit.web.cli as stcli
import logging

if __name__ == '__main__':
    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(stcli.main())
