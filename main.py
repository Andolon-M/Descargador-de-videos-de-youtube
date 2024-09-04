import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
import threading

def append_text(text_widget, text):
    text_widget.config(state=tk.NORMAL)
    text_widget.insert(tk.END, text + '\n')
    text_widget.config(state=tk.DISABLED)
    text_widget.see(tk.END)

def progress_hook(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes', 0)
        downloaded_bytes = d.get('downloaded_bytes', 0)
        if total_bytes > 0:
            progress = (downloaded_bytes / total_bytes) * 100
            progress_var.set(progress)
            root.update_idletasks()
        append_text(log_text, f"Downloading: {progress:.2f}%")

def download_video():
    url = url_entry.get()
    path = filedialog.askdirectory()
    
    if not url or not path:
        messagebox.showwarning("Input Error", "Please provide both a video URL and a download path.")
        return

    progress_var.set(0)  # Reset progress bar
    log_text.config(state=tk.NORMAL)
    log_text.delete(1.0, tk.END)  # Clear the log
    log_text.config(state=tk.DISABLED)

    def start_download():
        try:
            ydl_opts = {
                'outtmpl': f'{path}/%(title)s.%(ext)s',
                'format': 'best',
                'progress_hooks': [progress_hook],
                'quiet': True,  # Avoid printing info to stdout
                'noprogress': True  # Avoid printing the default progress bar
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            append_text(log_text, "Download completed!")
            messagebox.showinfo("Success", "Video downloaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error downloading video: {e}")
            append_text(log_text, f"Error: {e}")
            progress_var.set(0)

    # Run the download in a separate thread to prevent UI freezing
    threading.Thread(target=start_download).start()

# Create the GUI
root = tk.Tk()
root.title("YouTube Video Downloader")

# Set window background color and size
root.configure(bg="#2C3E50")
root.geometry("500x400")

# Add custom styles for labels and buttons
tk.Label(root, text="YouTube URL:", bg="#2C3E50", fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)

# Entry field with padding and background color
url_entry = tk.Entry(root, width=40, font=("Helvetica", 12), bg="#ECF0F1", fg="#2C3E50", bd=0)
url_entry.pack(pady=5, ipady=5)

# Styled download button
download_button = tk.Button(root, text="Download Video", bg="#E74C3C", fg="white", font=("Helvetica", 12, "bold"), relief="flat", padx=20, pady=5, command=download_video)
download_button.pack(pady=10)

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=10, fill='x')

# Text widget for logging progress messages
log_text = tk.Text(root, height=10, bg="#34495E", fg="white", font=("Courier", 9), state=tk.DISABLED, wrap='word')
log_text.pack(pady=10, fill='both', expand=True)

# Powered by label
powered_by_label = tk.Label(root, text="Powered by Andolon", bg="#2C3E50", fg="white", font=("Helvetica", 10, "italic"))
powered_by_label.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
