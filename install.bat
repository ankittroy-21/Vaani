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
echo    Installing dependencies... (Please wait)
echo.

:: ===== STEP 1: Verify Python =====
python --version >nul 2>&1 || (
    call :error "Python not found. Install Python 3.8-3.12 from python.org and check 'Add to PATH' during installation."
)

:: Get script directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

:: ===== STEP 2: Detect Python Version =====
for /f "delims=" %%i in ('python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"') do set PYVER=%%i
for /f "delims=" %%a in ('python -c "import struct; print(64 if struct.calcsize('P')*8==64 else 32)"') do set ARCH=%%a

echo Detected: Python %PYVER% (%ARCH%-bit)

:: Validate Python version
for /f "delims=" %%v in ('python -c "import sys; print(sys.version_info.major*10+sys.version_info.minor)"') do set PYNUM=%%v
if %PYNUM% lss 38 call :error "Vaani requires Python 3.8 or higher."
if %PYNUM% gtr 312 call :error "Vaani is not yet compatible with Python > 3.12."

:: ===== STEP 3: Install PyAudio =====
echo.
echo Installing PyAudio (voice processing engine)...

:: Define PyAudio wheel URLs
set "PYAUDIO_URLS="
set "PYAUDIO_URLS=^
3.8-64:https://mirrors.aliyun.com/pypi/packages/1e/dc/7fa93e20b0e6f4e25f629391b43a19813bca975f5eb2ed678cd2cf9a27d2/PyAudio-0.2.14-cp38-cp38-win_amd64.whl ^
3.8-32:https://mirrors.aliyun.com/pypi/packages/4a/41/274ea2a7f0470b04fcf6e9dbeec57d5aebbcfd30340acdbacaba8ee22dc5/PyAudio-0.2.14-cp38-cp38-win32.whl ^
3.9-64:https://mirrors.aliyun.com/pypi/packages/6e/3e/1e2e6a9d1734ff0fbbd8d8cb37e372802fa7b137f2cfa37a18d4e0a2dcb8/PyAudio-0.2.14-cp39-cp39-win_amd64.whl ^
3.9-32:https://mirrors.aliyun.com/pypi/packages/df/c8/61d70b38517a6761a2ef31b19c8b55a5cd7e88492241b86a438e7d3937cc/PyAudio-0.2.14-cp39-cp39-win32.whl ^
3.10-64:https://mirrors.aliyun.com/pypi/packages/d6/52/ccaf77077f40d7cc62c6e8cbfb79cf13c7e24858cb282a0bbab626940ada/PyAudio-0.2.14-cp310-cp310-win_amd64.whl ^
3.10-32:https://mirrors.aliyun.com/pypi/packages/ea/bf/b5b8da2f2012e6c82dd15d21e6e405d20b46994e20e3a7d021e07a620ec1/PyAudio-0.2.14-cp310-cp310-win32.whl ^
3.11-64:https://mirrors.aliyun.com/pypi/packages/83/f0/8f25f0b911f3b56aa7318d29fc034365a8208ea5cb856d508e87d01e8ff2/PyAudio-0.2.14-cp311-cp311-win_amd64.whl ^
3.11-32:https://mirrors.aliyun.com/pypi/packages/3e/18/82d22df540e29a0c248a79cfb16f0f9b0ad8a8dcd6ecf92b0e7a6a20a79e/PyAudio-0.2.14-cp311-cp311-win32.whl ^
3.12-64:https://mirrors.aliyun.com/pypi/packages/f3/7e/4493900aa3a60da0f0ac32cf63a1c020f9490b3a89d8a4c111d9a6bce7a/PyAudio-0.2.14-cp312-cp312-win_amd64.whl ^
3.12-32:https://mirrors.aliyun.com/pypi/packages/7e/f4/6292f2db2529c79d80167dfd49c2cbb16d32f5a79d2a3df7b59b7cb51f86/PyAudio-0.2.14-cp312-cp312-win32.whl"

:: Find the correct URL
set "WHL_URL="
for %%A in (%PYAUDIO_URLS%) do (
    for /f "tokens=1,2 delims=:" %%B in ("%%A") do (
        if "%%B"=="%PYVER%-%ARCH%" set "WHL_URL=%%C"
    )
)

if not defined WHL_URL (
    call :error "No PyAudio wheel found for Python %PYVER% (%ARCH%-bit)"
)

:: Download with multiple fallbacks
echo Downloading PyAudio...
(
    curl -sSL -o pyaudio.whl "%WHL_URL%" || (
        powershell -command "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile('%WHL_URL%', 'pyaudio.whl')" || (
            python -c "import urllib.request; urllib.request.urlretrieve('!WHL_URL!', 'pyaudio.whl')" || (
                call :error "Failed to download PyAudio from !WHL_URL!"
            )
        )
    )
) >nul 2>&1

:: Verify download
if not exist pyaudio.whl call :error "PyAudio wheel failed to download"
for %%F in (pyaudio.whl) do if %%~zF lss 100000 call :error "Downloaded PyAudio wheel is corrupted (too small)"

:: Install PyAudio
echo Installing PyAudio...
pip install --no-cache-dir pyaudio.whl || (
    call :error "PyAudio installation failed. Try:^
    1. Running as Administrator^
    2. Using 'python -m pip install pyaudio.whl'^
    3. Installing Microsoft Visual C++ Redistributable"
)
del pyaudio.whl 2>nul

:: ===== STEP 4: Install Requirements =====
echo.
echo Installing dependencies from requirements.txt...

if not exist "requirements.txt" (
    call :error "requirements.txt not found in: %SCRIPT_DIR%"
)

pip install -r requirements.txt || (
    call :error "Failed to install requirements. Check:^
    1. Internet connection^
    2. requirements.txt format"
)

:: ===== FINAL MESSAGE =====
echo.
echo    ==================================================================
echo     SUCCESS: All dependencies installed!
echo.
echo     Run 'main.py' to start Vaani Assistant
echo    ==================================================================
echo.
pause
