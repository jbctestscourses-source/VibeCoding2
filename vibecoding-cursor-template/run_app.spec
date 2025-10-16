from PyInstaller.utils.hooks import collect_all

# -*- mode: python ; coding: utf-8 -*-

datas_streamlit, binaries_streamlit, hiddenimports_streamlit = collect_all('streamlit')

a = Analysis(
    ['run_app.py'],
    pathex=[],
    binaries=[],
   wdatas=datas_streamlit + [('app.py', '.'), ('.env', '.')], # Inclui Metadados E os seus ficheiros
    hiddenimports=hiddenimports_streamlit + [], # Inclui hiddenimports do Streamlit
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='run_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='run_app',
)
