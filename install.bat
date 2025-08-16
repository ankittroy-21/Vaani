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

echo    ==================================================================
echo                 [STEP 1 of 2] : Installing Core Microphone Driver
echo    ==================================================================
echo.
echo    INFO: Installing 'PyAudio', the library that lets the assistant
echo          access your microphone.
echo.
echo    > ACTION: Installing from a pre-built package to avoid errors.
pause
echo.
pip install https://download.lfd.uci.edu/pythonlibs/archived/PyAudio-0.2.14-cp312-cp312-win_amd64.whl
echo.
echo    > SUCCESS: Core Microphone Driver installed successfully!
echo.
echo    Continuing to the next step in 5 seconds...
timeout /t 5 /nobreak >nul
cls

echo    ==================================================================
echo                 [STEP 2 of 2] : Installing Other Libraries
echo    ==================================================================
echo.
echo    INFO: Installing all other required libraries for features like
echo    deep-translator, SpeechRecognition, gTTS, requests and Wikipedia.
echo.
echo    > ACTION: Reading from 'requirements.txt' and installing packages.
echo.
pip install -r requirements.txt
echo.
echo    > SUCCESS: All required libraries have been installed!
echo.
echo    Finalizing setup in 4 seconds...
timeout /t 4 /nobreak >nul
cls

color 0F

echo    ==================================================================
echo                           SETUP COMPLETE!
echo    ==================================================================
echo.
echo                    Vaani is now ready to be used.
echo.
echo    To start the assistant, you can now run the 'main.py' script.
echo.
echo    Thank you for installing!
echo.
pause