from cx_Freeze import setup, Executable
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from mpl_toolkits.mplot3d import Axes3D
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

# Параметры скрипта
script_name = 'main.py'  # Имя вашего скрипта
executable_name = 'your_executable'  # Имя исполняемого файла (без расширения)

# Конфигурация cx-Freeze
executables = [Executable(script_name, base='Win32GUI')]

build_options = {
    'build_exe': {
        'includes': [
            'numpy.core._methods', 'numpy.lib.format', 'matplotlib.backends.backend_qt5agg',
            'scipy.integrate._ivp.ivp', 'mpl_toolkits.mplot3d', 'PyQt5.QtWidgets'
        ],
        'excludes': ['tkinter'],
        'optimize': 2
    }
}

# Создание исполняемого файла
setup(
    name='YourApp',
    version='1.0',
    description='Description of your app',
    options=build_options,
    executables=executables
)
