@echo off
setlocal EnableDelayedExpansion

:loop
echo Starting Twitch Viewer Bot...

:: Read settings from autosettings.txt
set /p option=<autosettings.txt
for /f "skip=1" %%a in (autosettings.txt) do (
    if not defined channel (
        set "channel=%%a"
    ) else if not defined viewers (
        set "viewers=%%a"
    )
)

:: Run the bot with automatic input
(
echo !option!
echo !channel!
echo !viewers!
) | python main.py

:: Wait a moment before restarting
timeout /t 5 /nobreak >nul

:: Loop back to start
goto loop