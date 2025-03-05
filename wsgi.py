import streamlit.cli as stcli
import sys

sys.argv = ["streamlit", "run", "app.py"]  # Reemplaza 'app.py' con el nombre de tu archivo principal
stcli.main()
