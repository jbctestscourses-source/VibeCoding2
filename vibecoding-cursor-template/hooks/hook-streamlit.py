# hooks/hook-streamlit.py

from PyInstaller.utils.hooks import collect_data_files, collect_all

# Usa collect_all para obter dados e metadados, e hiddenimports.
datas, binaries, hiddenimports = collect_all('streamlit')