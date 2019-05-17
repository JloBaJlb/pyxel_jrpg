NAME = "JRPG Base Core"
VERSION = "0.1"
DESCRIPTION = "Base core of JRPG-like games written on pyxel"
from OpenGL.raw.GL.SGIX import *


###########################################
import sys,os
from cx_Freeze import setup,Executable

additional_library = ['numpy.core._methods','numpy.lib.format']
PYTHON_PATH = os.path.dirname(sys.executable)
os.environ['TCL_LIBRARY'] = r'{}\tcl\tcl8.6'.format(PYTHON_PATH)
os.environ['TK_LIBRARY'] = r'{}\tcl\tcl8.6'.format(PYTHON_PATH)


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    executables=[Executable('init.py', base = "Win32GUI", targetName='GAME.exe'),
                 Executable('level1.py'),
                 Executable('main.py'),
                 Executable('main.py'),
                 Executable('monsters.py')
                 ],
    options={
            'build_exe': {
                'zip_exclude_packages': '*',
                'includes': additional_library,
                'packages': ['OpenGL'],
                'include_files': ['my_resource.pyxel', 'items.txt', 'monsters.txt'],
                }
            }, requires=['pyxel']
    )