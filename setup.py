from distutils.sysconfig import get_python_lib
from os.path import join
import sys


from cx_Freeze import setup, Executable   


#from generic.version import COMMIT_REVISION


ADD_INCLUDES = []
if sys.platform == "win32":
    ADD_INCLUDES = [join(get_python_lib(),  "cefpython3", "locales"),
                    join(get_python_lib(),  "cefpython3", "d3dcompiler_43.dll"),
                    join(get_python_lib(),  "cefpython3", "d3dcompiler_46.dll"),
                    join(get_python_lib(),  "cefpython3", "ffmpegsumo.dll"),
                    join(get_python_lib(),  "cefpython3", "icudt.dll"),
                    join(get_python_lib(),  "cefpython3", "libEGL.dll"),
                    join(get_python_lib(),  "cefpython3", "libGLESv2.dll"),
                    join(get_python_lib(),  "cefpython3", "cefclient.exe"),
                    (join(get_python_lib(),  "cefpython3", "subprocess.exe"), "SAV.exe"),
                    join(get_python_lib(),  "cefpython3", "cef.pak"),
                    join(get_python_lib(),  "cefpython3", "devtools_resources.pak"),
                   ]
#    else .. for LINUX, MAC ans so.on
build_exe_options = {"icon": "app.ico",  # some icon for exe from res folder
                     "packages": ["generic",
									"re",
									"urllib",
									"imaplib",
									"smtplib",
									"htql",
                                  "requests",
                                  "pickle",
                                  "base64",
                                  "threading",
                                  "os",
                                  "collections",
                                  "PyQt4",
                                  "cefpython3"
                                  # and others project speciffic modules
                                  ],
                     "excludes": ["PyQt4.QWebKit","PyQt4.uic.port_v3.proxy_base"], # exclude QWebKide, it is installed but we don't need this
                     "optimize": 2,
                     "compressed": True,
                     "include_files": ADD_INCLUDES,
                     "include_msvcr": True,
                     }
base = None
if sys.platform.startswith("win"):
    base = "Win32GUI"  #Win32GUI/Console for show stdout and stderr


setup(   
    name = "Smart Ad Viewer",   
    #version = str(COMMIT_REVISION / 10),   
    description = "Desc...",   
    options = {"build_exe": build_exe_options},
    executables = [Executable("application.py", base=base),
                  ]
)