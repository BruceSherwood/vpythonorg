from distutils.core import setup
import py2exe
 
includes = []
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter']
packages = []
dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll',
                'tk84.dll','w9xpopen.exe']
Data_Files = []
Data_Files.append ( ('', [r'C:\Python27\Lib\site-packages\visual_common\turbulence3.tga']))
Data_Files.append ( ('', [r'C:\Python27\Lib\site-packages\visual_common\wood.tga']))
Data_Files.append ( ('', [r'C:\Python27\Lib\site-packages\visual_common\BlueMarble.tga']))
Data_Files.append ( ('', [r'C:\Python27\Lib\site-packages\visual_common\brickbump.tga']))
Data_Files.append ( ('', [r'C:\Python27\Lib\site-packages\visual_common\earth.tga']))
Data_Files.append ( ('', [r'C:\Python27\Lib\site-packages\visual_common\random.tga']))

setup(
    name="PyStars",
    version="1.0",
    description="An exec Program",
    options = {"py2exe": {"compressed": 2, 
                          "optimize": 2,
                          "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          "bundle_files": 1,
                          "dist_dir": "dist",
                          "xref": False,
                          "skip_archive": False,
                          'dist_dir': "Python Exec",
                          "ascii": False,
                          "custom_boot_script": '',
                         }
              },
    zipfile = None,
    data_files = Data_Files,
    windows=[{"script":"stars.py",
            #"icon_resources":[(0, 'stars.ico')], 
            "dest_base": "Stars"}]
)

