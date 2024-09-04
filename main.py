import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
import os
import pickle
import threading
import time

# File to store the download path
CONFIG_FILE = "config.pkl"

def load_config():
    """Load the saved configuration."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'rb') as f:
            return pickle.load(f)
    return {}

def save_config(config):
    """Save the configuration."""
    with open(CONFIG_FILE, 'wb') as f:
        pickle.dump(config, f)

def update_progress_bar(downloaded_bytes, total_bytes):
    """Update the progress bar and status label."""
    if total_bytes > 0:
        progress = (downloaded_bytes / total_bytes) * 100
        progress_var.set(progress)
        root.update_idletasks()

def update_status(message):
    """Update the status label."""
    status_label.config(text=message)
    root.update_idletasks()

def progress_hook(d):
    """Handle progress and status updates."""
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes', 0)
        downloaded_bytes = d.get('downloaded_bytes', 0)
        update_progress_bar(downloaded_bytes, total_bytes)
        message = d.get('info_dict', {}).get('title', 'Downloading...')
        update_status(message)
    elif d['status'] == 'finished':
        update_status(f"Finished downloading: {d['filename']}")

def download_video():
    url = url_entry.get()
    path = download_path.get()  # Use the saved path
    
    if not url or not path:
        messagebox.showwarning("Input Error", "Please provide both a video URL and a download path.")
        return

    progress_var.set(0)  # Reset progress bar
    update_status("Starting download...")

    def download_task():
        try:
            ydl_opts = {
                'outtmpl': f'{path}/%(title)s.%(ext)s',
                'format': 'best',
                'progress_hooks': [progress_hook],
                'ffmpeg_location': 'C:/path/to/ffmpeg/bin',  # Replace with the path to your ffmpeg directory
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            messagebox.showinfo("Success", "Video downloaded successfully!")
            update_status("Download complete!")
        except Exception as e:
            messagebox.showerror("Error", f"Error downloading video: {e}")
            update_status("Download failed.")
            progress_var.set(0)  # Reset progress bar in case of error

    # Run the download task in a separate thread
    threading.Thread(target=download_task).start()

def download_mp3():
    url = url_entry.get()
    path = download_path.get()  # Use the saved path
    
    if not url or not path:
        messagebox.showwarning("Input Error", "Please provide both a video URL and a download path.")
        return

    progress_var.set(0)  # Reset progress bar
    update_status("Starting download...")

    def download_task():
        try:
            ydl_opts = {
                'outtmpl': f'{path}/%(title)s.%(ext)s',
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'progress_hooks': [progress_hook]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            messagebox.showinfo("Success", "Audio downloaded successfully!")
            update_status("Download complete!")
        except Exception as e:
            messagebox.showerror("Error", f"Error downloading audio: {e}")
            update_status("Download failed.")
            progress_var.set(0)  # Reset progress bar in case of error

    # Run the download task in a separate thread
    threading.Thread(target=download_task).start()

def set_download_path():
    """Open a dialog to select a download path and save it."""
    path = filedialog.askdirectory()
    if path:
        download_path.set(path)
        save_config({'download_path': path})

# Load saved configuration
config = load_config()
initial_path = config.get('download_path', '')

# Create the GUI
root = tk.Tk()
root.title("YouTube Downloader")

# Set window background color and size
root.configure(bg="#2C3E50")
root.geometry("450x450")

# Add custom styles for labels and buttons
tk.Label(root, text="YouTube URL:", bg="#2C3E50", fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)

# Entry field with padding and background color
url_entry = tk.Entry(root, width=40, font=("Helvetica", 12), bg="#ECF0F1", fg="#2C3E50", bd=0)
url_entry.pack(pady=5, ipady=5)

# Download path variable
download_path = tk.StringVar(value=initial_path)

# Entry field for download path with a button to change it
path_entry = tk.Entry(root, textvariable=download_path, width=40, font=("Helvetica", 12), bg="#ECF0F1", fg="#2C3E50", bd=0, state=tk.DISABLED)
path_entry.pack(pady=5, ipady=5)

# Button to change download path
change_path_button = tk.Button(root, text="Change Download Path", bg="#3498DB", fg="white", font=("Helvetica", 12, "bold"), relief="flat", padx=10, pady=5, command=set_download_path)
change_path_button.pack(pady=10)

# Styled download button for video
download_button = tk.Button(root, text="Download Video", bg="#E74C3C", fg="white", font=("Helvetica", 12, "bold"), relief="flat", padx=20, pady=5, command=download_video)
download_button.pack(pady=5)

# Styled download button for MP3
download_mp3_button = tk.Button(root, text="Download MP3", bg="#E67E22", fg="white", font=("Helvetica", 12, "bold"), relief="flat", padx=20, pady=5, command=download_mp3)
download_mp3_button.pack(pady=5)

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=300)  # Adjust length as needed
progress_bar.pack(pady=10, fill='x')

# Status label
status_label = tk.Label(root, text="", bg="#2C3E50", fg="white", font=("Helvetica", 10))
status_label.pack(pady=5)

# Powered by label
powered_by_label = tk.Label(root, text="Powered by Andolon", bg="#2C3E50", fg="white", font=("Helvetica", 10, "italic"))
powered_by_label.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
