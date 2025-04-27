from flask import Flask, render_template, request, send_from_directory, url_for, redirect, flash, session, send_file
import os
import uuid
import moviepy.editor as mp
import numpy as np
import math
import threading
import subprocess
import time
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.urandom(24)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB limit

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)
os.makedirs('static/icons', exist_ok=True)

# Add custom template filters
@app.template_filter('current_year')
def current_year_filter(text):
    return datetime.now().year

@app.template_filter('now')
def now_filter(format_string):
    return datetime.now().strftime(f'%{format_string}')

# Check if FFmpeg is installed
def is_ffmpeg_installed():
    try:
        subprocess.run(
            ["ffmpeg", "-version"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            check=True
        )
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

# Import pydub only if FFmpeg is installed
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Extract audio from video
def extract_audio(video_path, output_path, output_format, num_parts):
    try:
        # Extract audio from video
        video = mp.VideoFileClip(video_path)
        audio = video.audio

        output_filename = os.path.splitext(os.path.basename(video_path))[0]
        
        # If not splitting
        if num_parts == 1:
            full_output_path = os.path.join(output_path, f"{output_filename}.{output_format}")
            audio.write_audiofile(full_output_path)
            video.close()
            return [full_output_path]
            
        # If splitting into parts
        if PYDUB_AVAILABLE:
            # First, export as WAV for processing
            temp_wav = os.path.join(output_path, f"{output_filename}_temp.wav")
            audio.write_audiofile(temp_wav)
            video.close()
            
            # Load with pydub for splitting
            sound = AudioSegment.from_wav(temp_wav)
            
            # Calculate part duration
            part_length_ms = len(sound) // num_parts
            
            # Split and export parts
            output_files = []
            for i in range(num_parts):
                start_time = i * part_length_ms
                end_time = (i + 1) * part_length_ms if i < num_parts - 1 else len(sound)
                
                part = sound[start_time:end_time]
                part_filename = os.path.join(output_path, f"{output_filename}_part{i+1}.{output_format}")
                
                part.export(part_filename, format=output_format)
                output_files.append(part_filename)
            
            # Remove temporary WAV file
            os.remove(temp_wav)
            
            return output_files
    except Exception as e:
        raise Exception(f"Error extracting audio: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html', 
                          ffmpeg_installed=is_ffmpeg_installed(),
                          pydub_available=PYDUB_AVAILABLE)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/sw.js')
def service_worker():
    return send_from_directory('static', 'sw.js')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['video']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Generate a secure filename with UUID to prevent collisions
        original_filename = secure_filename(file.filename)
        filename = f"{uuid.uuid4()}_{original_filename}"
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Get form data
        output_format = request.form.get('format', 'mp3')
        num_parts = int(request.form.get('parts', 1))
        
        # Create a unique output directory for this job
        job_id = str(uuid.uuid4())
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], job_id)
        os.makedirs(output_path, exist_ok=True)
        
        try:
            # Process the file
            output_files = extract_audio(file_path, output_path, output_format, num_parts)
            
            # Store info in session
            session['job_id'] = job_id
            session['output_files'] = [os.path.basename(f) for f in output_files]
            session['original_filename'] = os.path.splitext(original_filename)[0]
            
            # Clean up the input file
            if os.path.exists(file_path):
                os.remove(file_path)
                
            return redirect(url_for('results'))
        
        except Exception as e:
            flash(f"Error processing file: {str(e)}")
            # Clean up
            if os.path.exists(file_path):
                os.remove(file_path)
            return redirect(url_for('index'))
    
    else:
        flash('Invalid file type. Please upload a video file (mp4, avi, mkv, etc.)')
        return redirect(url_for('index'))

@app.route('/results')
def results():
    job_id = session.get('job_id')
    output_files = session.get('output_files', [])
    original_filename = session.get('original_filename', 'Unknown')
    
    if not job_id or not output_files:
        flash('No processing results found')
        return redirect(url_for('index'))
    
    return render_template('results.html', 
                          job_id=job_id,
                          output_files=output_files,
                          original_filename=original_filename)

@app.route('/download/<job_id>/<filename>')
def download(job_id, filename):
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], job_id)
    return send_from_directory(output_path, filename, as_attachment=True, 
                              mimetype='application/octet-stream')

# Scheduled job to clean up old files (runs in background)
def cleanup_old_files():
    while True:
        try:
            # Sleep for 1 hour before each cleanup
            time.sleep(3600)
            
            now = time.time()
            # Clean output folders older than 24 hours
            for job_id in os.listdir(app.config['OUTPUT_FOLDER']):
                job_path = os.path.join(app.config['OUTPUT_FOLDER'], job_id)
                if os.path.isdir(job_path):
                    created_time = os.path.getctime(job_path)
                    if now - created_time > 24 * 3600:  # 24 hours
                        for file in os.listdir(job_path):
                            try:
                                os.remove(os.path.join(job_path, file))
                            except:
                                pass
                        try:
                            os.rmdir(job_path)
                        except:
                            pass
                            
            # Clean uploads folder (anything older than 2 hours)
            for file in os.listdir(app.config['UPLOAD_FOLDER']):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
                if os.path.isfile(file_path):
                    created_time = os.path.getctime(file_path)
                    if now - created_time > 2 * 3600:  # 2 hours
                        try:
                            os.remove(file_path)
                        except:
                            pass
        except Exception as e:
            print(f"Error in cleanup job: {str(e)}")

if __name__ == '__main__':
    # Start cleanup thread
    cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
    cleanup_thread.start()
    
    # Start the Flask app
    app.run(debug=True, threaded=True) 