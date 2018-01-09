# -*- mode: python -*-

def get_cefpython_path():
    import cefpython3 as cefpython

    path = os.path.dirname(cefpython.__file__)
    return "%s%s" % (path, os.sep)

cefp = get_cefpython_path()

a = Analysis(['application.py'],
             hiddenimports=["json.decoder", "json.scanner", "json.encoder","htql.pyd"])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='SmartAdViewer.exe',
          debug=False,
          strip=None,
          upx=False,
          console=False,
		  icon='app.ico')
coll = COLLECT(exe,
               a.binaries + [('icudt.dll', '%s/icudt.dll' % cefp, 'BINARY'),('libcef.dll', '%s/libcef.dll' % cefp, 'BINARY'),('ffmpegsumo.dll', '%s/ffmpegsumo.dll' % cefp, 'BINARY'),('d3dcompiler_46.dll', '%s/d3dcompiler_46.dll' % cefp, 'BINARY'),('d3dcompiler_43.dll', '%s/d3dcompiler_43.dll' % cefp, 'BINARY')],
               a.zipfiles,
               a.datas + [('locales/en-US.pak', '%s/locales/en-US.pak' % cefp, 'DATA'),('cef.pak', '%s/cef.pak' % cefp, 'DATA'), ('subprocess.exe','%s/subprocess.exe' % cefp,'DATA'),('cefclient.exe','%s/cefclient.exe' % cefp,'DATA')],
               strip=None,
               upx=False,
               name='application')