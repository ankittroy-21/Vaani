@echo off
cls
title Vaani Assistant Installer
color 0A

echo.
echo    ==================================================================
echo                         V A A N I  ASSISTANT
echo                      -- Voice-Powered Knowledge --
echo    ==================================================================
echo                   (Made by Group Number 9 From CSE 3C)
echo.
echo    Welcome! This script will automatically install all the necessary
echo    components for Vaani.
echo.
pause

:: Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not added to PATH.
    echo Please install Python 3.8 - 3.12 and re-run this installer.
    pause
    exit /b
)

:: Upgrade pip
pip install --upgrade pip

:: Detect Python version (major.minor)
for /f "delims=" %%i in ('python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"') do set PYVER=%%i
:: Detect architecture (32/64 bit)
for /f "delims=" %%a in ('python -c "import struct; print(struct.calcsize('P')*8)"') do set ARCH=%%a

echo Detected Python version: %PYVER%
echo Detected Python architecture: %ARCH%-bit
echo.

:: Guard: Require 3.8 <= Python <= 3.12
for /f "delims=" %%v in ('python -c "import sys; print(sys.version_info.major*10+sys.version_info.minor)"') do set PYNUM=%%v
if %PYNUM% LSS 38 (
    echo ERROR: Vaani requires Python 3.8 or higher.
    echo Please install Python 3.8 - 3.12.
    pause
    exit /b
)

if %PYNUM% GTR 312 (
    echo ERROR: Vaani is not yet compatible with Python versions above 3.12.
    echo Please install Python 3.8 - 3.12.
    pause
    exit /b
)

set PYAUDIO_INSTALLED=0
set WHL_URL=

if "%PYVER%"=="3.12" (
    if "%ARCH%"=="64" (
        set WHL_URL=https://mirrors.aliyun.com/pypi/packages/f3/7e/4493900aa3a60da0f0ac32cf63a1c020f9490b3a89d8a4c111d9a6bce7a/PyAudio-0.2.14-cp312-cp312-win_amd64.whl
    ) else (
        set WHL_URL=https://mirrors.aliyun.com/pypi/packages/7e/f4/6292f2db2529c79d80167dfd49c2cbb16d32f5a79d2a3df7b59b7cb51f86/PyAudio-0.2.14-cp312-cp312-win32.whl
    )
)

if "%PYVER%"=="3.11" (
    if "%ARCH%"=="64" (
        set WHL_URL=https://mirrors.aliyun.com/pypi/packages/83/f0/8f25f0b911f3b56aa7318d29fc034365a8208ea5cb856d508e87d01e8ff2/PyAudio-0.2.14-cp311-cp311-win_amd64.whl
    ) else (
        set WHL_URL=https://mirrors.aliyun.com/pypi/packages/3e/18/82d22df540e29a0c248a79cfb16f0f9b0ad8a8dcd6ecf92b0e7a6a20a79e/PyAudio-0.2.14-cp311-cp311-win32.whl
    )
)

if "%PYVER%"=="3.10" (
    if "%ARCH%"=="64" (
        set WHL_URL=https://mirrors.aliyun.com/pypi/packages/d6/52/ccaf77077f40d7cc62c6e8cbfb79cf13c7e24858cb282a0bbab626940ada/PyAudio-0.2.14-cp310-cp310-win_amd64.whl
    ) else (
        set WHL_URL=https://mirrors.aliyun.com/pypi/packages/ea/bf/b5b8da2f2012e6c82dd15d21e6e405d20b46994e20e3a7d021e07a620ec1/PyAudio-0.2.14-cp310-cp310-win32.whl
    )
)

if "%PYVER%"=="3.9" (
    if "%ARCH%"=="64" (
        set WHL_URL=https://mirrors.aliyun.com/pypi/packages/6e/3e/1e2e6a9d1734ff0fbbd8d8cb37e372802fa7b137f2cfa37a18d4e0a2dcb8/PyAudio-0.2.14-cp39-cp39-win_amd64.whl
    ) else (
        set WHL_URL=https://mirrors.aliyun.com/pypi/packages/df/c8/61d70b38517a6761a2ef31b19c8b55a5cd7e88492241b86a438e7d3937cc/PyAudio-0.2.14-cp39-cp39-win32.whl
    )
)

if "%PYVER%"=="3.8" (
    if "%ARCH%"=="64" (
        set WHL_URL=https://mirrors.aliyun.com/pypi/packages/1e/dc/7fa93e20b0e6f4e25f629391b43a19813bca975f5eb2ed678cd2cf9a27d2/PyAudio-0.2.14-cp38-cp38-win_amd64.whl
    ) else (
        set WHL_URL=https://mirrors.aliyun.com/pypi/packages/4a/41/274ea2a7f0470b04fcf6e9dbeec57d5aebbcfd30340acdbacaba8ee22dc5/PyAudio-0.2.14-cp38-cp38-win32.whl
    )
)

:: Download & install PyAudio
if defined WHL_URL (
    echo Downloading PyAudio wheel...
    curl -sSL -o "pyaudio.whl" "%WHL_URL%"
    if not exist "pyaudio.whl" (
        echo ERROR: Failed to download PyAudio wheel.
        pause
        exit /b
    )
    echo Installing PyAudio from downloaded wheel...
    pip install "pyaudio.whl" && set PYAUDIO_INSTALLED=1
    if exist "pyaudio.whl" del "pyaudio.whl"
)

if "%PYAUDIO_INSTALLED%"=="0" (
    echo ERROR: PyAudio installation failed.
    echo Please ensure you are using Python 3.8 - 3.12 (32/64-bit).
    pause
    exit /b
)

echo.
echo    ==================================================================
echo     [STEP 2] : Installing Other Dependencies
echo    ==================================================================
echo.

pip install -r requirements.txt

echo.
echo    ==================================================================
echo     Installation Complete! Vaani is Ready
echo     To start the assistant, you can now run the 'main.py' script.
echo.
echo                     Thank you for installing!
echo    ==================================================================
pause