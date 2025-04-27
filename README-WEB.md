# Audio Extractor - Web Version

This is the web version of the Audio Extractor application which allows users to extract audio from video files via a browser interface.

## Features

- Extract audio from various video formats (mp4, avi, mkv, etc.)
- Choose the output audio format (mp3, wav, ogg, flac)
- Split the extracted audio into multiple equal parts
- Download extracted audio directly from the browser
- User-friendly web interface

## Requirements

- Python 3.6 or higher
- Dependencies listed in requirements.txt
- **FFmpeg** (required for audio processing)

## Local Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. **Install FFmpeg** (REQUIRED):

   - **Windows**: 
     1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) or [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (recommended for Windows)
     2. Extract the ZIP file to a location on your computer (e.g., `C:\ffmpeg`)
     3. Add the `bin` folder to your PATH environment variable

   - **macOS**:
     ```bash
     brew install ffmpeg
     ```

   - **Linux (Ubuntu/Debian)**:
     ```bash
     sudo apt update
     sudo apt install ffmpeg
     ```

## Local Usage

1. Run the application:

```bash
python app.py
```

2. Open your browser and navigate to http://localhost:5000
3. Upload a video file
4. Select your preferred audio format and number of parts
5. Click "Extract Audio" to process
6. Download the processed audio files

## Deployment Options

### Deploying to Heroku

1. Create a new Heroku app:

```bash
heroku create your-app-name
```

2. Add the FFmpeg buildpack:

```bash
heroku buildpacks:add https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
heroku buildpacks:add heroku/python
```

3. Push to Heroku:

```bash
git push heroku main
```

### Deploying to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the build:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. Add the following environment variable:
   - KEY: `PATH`
   - VALUE: `PATH:/opt/render/project/bin:${PATH}`
5. Under Advanced settings, add a Custom Docker Command:
   ```
   apt-get update && apt-get install -y ffmpeg
   ```

### Deploying to PythonAnywhere

1. Sign up for a PythonAnywhere account
2. Upload your code or clone from Git
3. Set up a web app with Flask
4. Install FFmpeg:
   - Use the PythonAnywhere bash console
   - Request FFmpeg installation from PythonAnywhere support if you're on a free plan, or install it on paid plans
5. Configure your WSGI file to point to `app.py`

## Notes

- Processing large videos will take more time and resources
- Some hosting providers have memory and time limits for free plans
- Ensure your hosting provider supports FFmpeg installation
- The upload file size limit is 500MB by default, which can be adjusted in the code 