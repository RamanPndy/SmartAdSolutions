# -*- mode: python -*-
a = Analysis(['application.py'],
             pathex=['E:\\SAV Installer\\src-trail'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='application.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
