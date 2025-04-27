# Audio Extractor

A simple application to extract audio from video files with the option to split into multiple parts.

## Features

- Extract audio from various video formats (mp4, avi, mkv, etc.)
- Choose the output audio format (mp3, wav, ogg, flac)
- Split the extracted audio into multiple equal parts
- User-friendly graphical interface

## Requirements

- Python 3.6 or higher
- Dependencies listed in requirements.txt
- **FFmpeg** (required for audio processing)

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. **Install FFmpeg** (REQUIRED):

   - **Windows**: 
     1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) or [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (recommended for Windows)
     2. Extract the ZIP file to a location on your computer (e.g., `C:\ffmpeg`)
     3. Add the `bin` folder to your PATH environment variable:
        - Right-click on "This PC" → Properties → Advanced system settings → Environment Variables
        - Edit the "Path" variable and add the path to the bin folder (e.g., `C:\ffmpeg\bin`)
        - Restart your command prompt or computer

   - **macOS**:
     ```
     brew install ffmpeg
     ```

   - **Linux (Ubuntu/Debian)**:
     ```
     sudo apt update
     sudo apt install ffmpeg
     ```

## Usage

1. Run the application:

```
python audio_extractor.py
```

2. Select a video file using the "Browse" button
3. Choose an output directory
4. Select your preferred audio format
5. Specify the number of parts to split the audio into (1 = no splitting)
6. Click "Extract Audio" to start the process
7. Wait for the extraction to complete

## Troubleshooting

If you encounter the error `[WinError 2] The system cannot find the file specified`, it means FFmpeg is not properly installed or not in your PATH. Please follow the FFmpeg installation instructions above.

## Additional Notes

- For MP3 or OGG file exports, you must have FFmpeg installed on your system
- The application splits audio into equal-length segments
- Large video files may take longer to process 