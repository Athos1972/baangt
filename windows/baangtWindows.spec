# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['..\\baangtIA.py'],
             pathex=['windows'],
             binaries=[],
             datas=[('../baangt/ressources/baangtLogo2020Small.png', 'ressources'),
                    ('../examples/', 'examples'),
                    ('../browsermob-proxy','browsermob-proxy')],
             hiddenimports=["cffi"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=False,
          windowed=True,
          name='baangt',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='baangt')
