import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
import moviepy.editor as mp
import numpy as np
import math
import sys
import subprocess

# Check if FFmpeg is installed
def is_ffmpeg_installed():
    try:
        # Try to run ffmpeg -version command
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

class AudioExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Extractor")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("TLabel", font=("Arial", 10))
        
        # Check dependencies
        self.ffmpeg_installed = is_ffmpeg_installed()
        
        self.create_widgets()
        
        # Show warning if dependencies are missing
        if not self.ffmpeg_installed:
            messagebox.showwarning(
                "Missing Dependencies", 
                "FFmpeg is not installed or not found in your PATH.\n\n"
                "Please install FFmpeg and make sure it's in your system PATH variable:\n"
                "1. Download from https://ffmpeg.org/download.html\n"
                "2. Add the bin directory to your system PATH\n"
                "3. Restart this application"
            )
        
        if not PYDUB_AVAILABLE:
            messagebox.showwarning(
                "Missing Dependencies", 
                "PyDub is not installed. Audio splitting will not be available.\n\n"
                "Please install it using: pip install pydub"
            )
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Video selection
        video_frame = ttk.Frame(main_frame)
        video_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(video_frame, text="Video File:").grid(row=0, column=0, sticky=tk.W)
        
        self.video_path_var = tk.StringVar()
        ttk.Entry(video_frame, textvariable=self.video_path_var, width=40).grid(row=0, column=1, padx=5)
        
        ttk.Button(video_frame, text="Browse", command=self.browse_video).grid(row=0, column=2, padx=5)
        
        # Output directory selection
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(output_frame, text="Output Directory:").grid(row=0, column=0, sticky=tk.W)
        
        self.output_path_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_path_var, width=40).grid(row=0, column=1, padx=5)
        
        ttk.Button(output_frame, text="Browse", command=self.browse_output).grid(row=0, column=2, padx=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.pack(fill=tk.X, pady=10)
        
        # Output format
        ttk.Label(options_frame, text="Output Format:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.format_var = tk.StringVar(value="mp3")
        format_combo = ttk.Combobox(options_frame, textvariable=self.format_var, width=10)
        format_combo['values'] = ('mp3', 'wav', 'ogg', 'flac')
        format_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Number of parts
        ttk.Label(options_frame, text="Split into parts:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.parts_var = tk.IntVar(value=1)
        parts_spin = ttk.Spinbox(options_frame, from_=1, to=100, textvariable=self.parts_var, width=10)
        parts_spin.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Progress frame
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(progress_frame, variable=self.progress_var, length=100)
        self.progress.pack(fill=tk.X, pady=5)
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        status_label.pack(pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.extract_button = ttk.Button(button_frame, text="Extract Audio", command=self.start_extraction)
        self.extract_button.pack(side=tk.RIGHT, padx=5)
        
        # Disable extract button if dependencies are missing
        if not self.ffmpeg_installed:
            self.extract_button["state"] = "disabled"
            self.status_var.set("FFmpeg not found. Please install FFmpeg.")
        
    def browse_video(self):
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=(
                ("Video files", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm"),
                ("All files", "*.*")
            )
        )
        if file_path:
            self.video_path_var.set(file_path)
            
    def browse_output(self):
        dir_path = filedialog.askdirectory(title="Select Output Directory")
        if dir_path:
            self.output_path_var.set(dir_path)
            
    def start_extraction(self):
        video_path = self.video_path_var.get()
        output_dir = self.output_path_var.get()
        
        if not video_path or not os.path.exists(video_path):
            messagebox.showerror("Error", "Please select a valid video file.")
            return
            
        if not output_dir or not os.path.exists(output_dir):
            messagebox.showerror("Error", "Please select a valid output directory.")
            return
        
        # Check if pydub is available when trying to split
        num_parts = self.parts_var.get()
        if num_parts > 1 and not PYDUB_AVAILABLE:
            messagebox.showerror(
                "Error", 
                "PyDub is required for splitting audio. Please install it with:\n\npip install pydub"
            )
            return
            
        # Start extraction in a new thread
        threading.Thread(target=self.extract_audio, daemon=True).start()
        
    def extract_audio(self):
        try:
            video_path = self.video_path_var.get()
            output_dir = self.output_path_var.get()
            output_format = self.format_var.get()
            num_parts = self.parts_var.get()
            
            # Update status
            self.status_var.set("Loading video...")
            self.progress_var.set(0)
            self.root.update_idletasks()
            
            # Extract audio from video
            try:
                video = mp.VideoFileClip(video_path)
            except Exception as e:
                if "ffmpeg" in str(e).lower():
                    messagebox.showerror(
                        "FFmpeg Error", 
                        "Error with FFmpeg. Make sure FFmpeg is installed correctly and in your PATH."
                    )
                    self.status_var.set("Error: FFmpeg not found or not working")
                    return
                else:
                    raise
            
            # Get base filename without extension
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            
            # Update status
            self.status_var.set("Extracting audio...")
            self.progress_var.set(30)
            self.root.update_idletasks()
            
            # Get audio
            audio = video.audio
            if audio is None:
                messagebox.showerror("Error", "No audio track found in this video.")
                self.status_var.set("No audio track found")
                video.close()
                return
            
            # Create a temporary wav file
            temp_audio_path = os.path.join(output_dir, f"{base_name}_temp.wav")
            audio.write_audiofile(temp_audio_path, logger=None)
            
            self.progress_var.set(60)
            self.root.update_idletasks()
            
            if num_parts > 1:
                self.status_var.set(f"Splitting audio into {num_parts} parts...")
                
                # Load audio file with pydub
                audio_segment = AudioSegment.from_file(temp_audio_path)
                
                # Calculate part duration
                total_duration = len(audio_segment)
                part_duration = math.ceil(total_duration / num_parts)
                
                # Split and save parts
                for i in range(num_parts):
                    self.status_var.set(f"Processing part {i+1} of {num_parts}...")
                    self.progress_var.set(60 + (i / num_parts) * 35)
                    self.root.update_idletasks()
                    
                    start_time = i * part_duration
                    end_time = min((i + 1) * part_duration, total_duration)
                    
                    part = audio_segment[start_time:end_time]
                    output_path = os.path.join(output_dir, f"{base_name}_part{i+1}.{output_format}")
                    part.export(output_path, format=output_format)
                
                # Remove temporary file
                os.remove(temp_audio_path)
                
            else:
                self.status_var.set("Converting audio...")
                
                # Just convert the format if needed
                if output_format != "wav":
                    audio_segment = AudioSegment.from_file(temp_audio_path)
                    output_path = os.path.join(output_dir, f"{base_name}.{output_format}")
                    audio_segment.export(output_path, format=output_format)
                    os.remove(temp_audio_path)
                else:
                    # Rename the temporary file
                    output_path = os.path.join(output_dir, f"{base_name}.wav")
                    os.rename(temp_audio_path, output_path)
            
            # Close video object
            video.close()
            
            self.progress_var.set(100)
            self.status_var.set("Extraction completed successfully!")
            messagebox.showinfo("Success", "Audio extraction completed successfully!")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioExtractorApp(root)
    root.mainloop() 