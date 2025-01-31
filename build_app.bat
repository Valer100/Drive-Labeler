@echo off
title Building Volume Labeler...

echo (1/4) Deleting temporary files...
echo.

rmdir /q /s "build"
rmdir /q /s "dist"
del /f /q "volume_labeler.spec"

echo.
echo (2/4) Installing dependencies...
echo.

python -m pip install -r requirements.txt
python -m pip install pyinstaller

echo.
echo (3/4) Building with PyInstaller...
echo.

python -m PyInstaller main.pyw --onedir --icon icon.ico --version-file "version.txt" --name "volume_labeler" --add-data "icons;./icons/" --add-data "icon.ico;." --add-data "icons.icl;." --add-data "OPEN_SOURCE_LICENSES.txt;." --exclude-module "numpy" --exclude-module "setuptools" --exclude-module "wheel" --exclude-module "importlib_metadata" --exclude-module "markupsafe" --exclude-module Pythonwin --exclude-module "win32" --exclude-module "win32com" --exclude-module "pywin32_system32"

echo .
echo (4/4) Deleting temporary files...
echo.

rmdir /q /s "build"
rmdir /q /s "dist/volume_labeler/_internal/pywin32_system32"
rmdir /q /s "dist/volume_labeler/_internal/win32"
del /f /q "volume_labeler.spec"
ren "dist" "build"

echo.
echo Volume Labeler has been successfully built.