@echo off
echo Setting up environment...
set PATH=%PATH%;C:\ffmpeg\bin

echo Installing dependencies...
python -m pip install -r requirements.txt

echo Starting Audio Extractor Web App...
python app.py
pause 