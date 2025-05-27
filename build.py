from cx_Freeze import setup, Executable

# Archivos adicionales (como recursos)
include_files = ['res/']

# Configuración del ejecutable
executables = [
    Executable("main.py", base="Win32GUI", target_name="suika.exe", icon='res/icon.ico')
]

# Setup de cx_Freeze
setup(
    name="Suika Game",
    version="1.0",
    description="Proyecto de la asignatura de Sistemas Multimedia de la UJA",
    options={
        "build_exe": {
            "include_files": include_files,
            "build_exe": "build/output",  # Usamos una carpeta temporal para los archivos de construcción
        }
    },
    executables=executables
)