@echo off

REM Controlla se Python è installato
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python è già installato.
) else (
    echo Python non è installato.
    choice /C YN /M "Desideri installare Python?"
    if %errorlevel% equ 1 (
        REM Scarica l'ultimo programma di installazione di Python
        echo Scaricamento del programma di installazione di Python...
        curl -O https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe

        REM Installa Python
        echo Installazione di Python...
        start python-3.11.4-amd64.exe /quiet InstallAllUsers=1 PrependPath=1

        REM Attendere il completamento dell'installazione di Python
        echo Attendere il completamento dell'installazione di Python...
        timeout 30 >nul

        REM Elimina il programma di installazione di Python
        del python-3.11.4-amd64.exe-

        echo Installazione di Python completata.
    ) else (
        echo Installazione di Python annullata.
    )
)

REM Installa le librerie richieste
echo Installazione delle librerie richieste...
pip install -r requirements.txt

echo Installazione completata.
pause
