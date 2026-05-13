# -*- mode: python ; coding: utf-8 -*-

# NOTE on `.env` bundling:
# The `.env` file referenced below is bundled INTO the distributed executable.
# Do NOT use your local development `.env` for production builds. Before running
# PyInstaller for a production release, replace the repo-level `.env` with the
# real production values. Real secrets must never be committed to the repository.

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('src/assets', 'src/assets'), ('.env', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    onefile=True,
)
