# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = [('assets/*.png','assets'), ('assets/music/*.wav', 'assets/music'), ('util/*', 'util'), ('scenes/*.py', 'scenes')]
datas += collect_data_files('assets')
datas += collect_data_files('assets/music')
datas += collect_data_files('util')
datas += collect_data_files('scenes')


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=['C:\\python39\\lib\\site-packages', 'C:\\Users\\shawn\\AppData\\Local\\Programs\\Python\\Python38\\Lib\\site-packages'],
    binaries=[],
    datas=datas,
    hiddenimports=['pygame-menu'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
