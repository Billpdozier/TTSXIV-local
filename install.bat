set venv=TTSXIV

call %USERPROFILE%\Anaconda3\Scripts\activate %USERPROFILE%\Anaconda3
call conda env create -f environment.yml
pause