@echo off
echo Setting up environment...
set PATH=%PATH%;C:\ffmpeg\bin

echo Installing dependencies...
python -m pip install moviepy pydub numpy

echo Starting Audio Extractor...
python audio_extractor.py
pause 