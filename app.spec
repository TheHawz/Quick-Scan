# -*- mode: python -*-

block_cipher = None

a = Analysis(['bin/app'],
             pathex=['.'],
             binaries=None,
             datas=[],
             hiddenimports=['PySide2.QtXml'],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Quick Scan',
          debug=True,
          strip=False,
          upx=True,
          console=True,
          icon='resources\\icons\\app.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Quick Scan')

app = BUNDLE(coll,
             name='Quick Scan.app',
             icon='resources/icons/app.icns',
             bundle_identifier=None)