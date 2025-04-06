import PyInstaller.__main__
import os
import shutil

# Clean previous builds
if os.path.exists('dist'):
    shutil.rmtree('dist')
if os.path.exists('build'):
    shutil.rmtree('build')

# Build the executable
PyInstaller.__main__.run([
    'main_for_build.py',
    '--onefile',
    '--windowed',
    '--icon=gtcd.ico',
    '--name=GTCD',
    # Critical hidden imports
    '--hidden-import=cv2',
    '--hidden-import=cv2.data',
    '--hidden-import=google.generativeai',
    '--hidden-import=customtkinter',
    '--hidden-import=pynput.keyboard._win32',  # Windows specific
    '--hidden-import=pynput.mouse._win32',
    '--hidden-import=pygetwindow',
    '--hidden-import=PIL',
    '--hidden-import=numpy',
    # Additional dependencies
    '--hidden-import=fpdf',
    '--hidden-import=textwrap',
    '--hidden-import=datetime',
    # OpenCV specific fixes
    '--collect-data=cv2',
    '--collect-data=google',
    # Path to your Python installation
    '--paths=C:\\Users\\prana\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages'
])