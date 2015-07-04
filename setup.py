from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('Main-GUI.py', base=base, targetName = 'siuewpasetup')
]

setup(name='SIUE WPA SETUP LINUX GUI',
      version = '1.0',
      description = 'Setup SIUE WPA on Linux using DBUS and Network Manager',
      options = dict(build_exe = buildOptions),
      executables = executables)
