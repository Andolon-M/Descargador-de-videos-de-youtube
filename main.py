import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp

def download_video():
    url = url_entry.get()
    path = filedialog.askdirectory()
    if not url or not path:
        messagebox.showwarning("Input Error", "Please provide both a video URL and a download path.")
        return

    try:
        ydl_opts = {
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'format': 'best'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Video downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error downloading video: {e}")

# Create the GUI
root = tk.Tk()
root.title("YouTube Video Downloader")

# Set window background color and size
root.configure(bg="#2C3E50")
root.geometry("400x200")

# Add custom styles for labels and buttons
tk.Label(root, text="YouTube URL:", bg="#2C3E50", fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)

# Entry field with padding and background color
url_entry = tk.Entry(root, width=40, font=("Helvetica", 12), bg="#ECF0F1", fg="#2C3E50", bd=0)
url_entry.pack(pady=5, ipady=5)

# Styled download button
download_button = tk.Button(root, text="Download Video", bg="#E74C3C", fg="white", font=("Helvetica", 12, "bold"), relief="flat", padx=20, pady=5, command=download_video)
download_button.pack(pady=20)

root.mainloop()
