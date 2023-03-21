set venv=TTSXIV

call %USERPROFILE%\Anaconda3\Scripts\activate %USERPROFILE%\Anaconda3
call activate %venv%

:: Change directory to the relative path that's needed for script
cd %~dp0

:: Run script at this location
call %USERPROFILE%/Anaconda3/envs/%venv%/python.exe "%~dp0\client.py"
PAUSE