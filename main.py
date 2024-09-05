import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
import os
import pickle
import threading

# Archivo para almacenar la ruta de descarga
CONFIG_FILE = "config.pkl"

# Variable global para controlar la cancelación
cancel_download = threading.Event()

def load_config():
    """
    Cargar la configuración guardada desde un archivo pickle.
    
    Retorna:
        dict: Diccionario de configuración con ajustes guardados.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'rb') as f:
            return pickle.load(f)
    return {}

def save_config(config):
    """
    Guardar la configuración en un archivo pickle.
    
    Args:
        config (dict): Diccionario de configuración a guardar.
    """
    with open(CONFIG_FILE, 'wb') as f:
        pickle.dump(config, f)

def update_progress_bar(downloaded_bytes, total_bytes):
    """
    Actualiza la barra de progreso y la etiqueta de estado basado en los bytes descargados.
    
    Args:
        downloaded_bytes (int): Número de bytes descargados.
        total_bytes (int): Número total de bytes a descargar.
    """
    if total_bytes > 0:
        progress = (downloaded_bytes / total_bytes) * 100
        progress_var.set(progress)
        root.update_idletasks()

def update_status(message):
    """
    Actualiza la etiqueta de estado con un mensaje.
    
    Args:
        message (str): El mensaje a mostrar en la etiqueta de estado.
    """
    status_label.config(text=message)
    root.update_idletasks()

def progress_hook(d):
    """
    Función hook para manejar actualizaciones de progreso y verificar cancelación.
    
    Args:
        d (dict): Diccionario que contiene la información del progreso.
    """
    if cancel_download.is_set():
        raise Exception("Descarga cancelada")

    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes', 0)
        downloaded_bytes = d.get('downloaded_bytes', 0)
        update_progress_bar(downloaded_bytes, total_bytes)
        message = d.get('info_dict', {}).get('title', 'Descargando...')
        update_status(message)
    elif d['status'] == 'finished':
        update_status(f"Descarga finalizada: {d['filename']}")
        progress_var.set(100)
        root.update_idletasks()

def download_video():
    """
    Descarga el video desde la URL proporcionada y lo guarda en la ruta seleccionada.
    """
    url = url_entry.get()
    path = download_path.get()  # Usa la ruta guardada
    
    if not url or not path:
        messagebox.showwarning("Error de entrada", "Por favor, proporcione una URL de video y una ruta de descarga.")
        return

    progress_var.set(0)  # Restablecer barra de progreso
    update_status("Iniciando descarga...")
    cancel_download.clear()  # Limpiar el evento de cancelación

    def download_task():
        """
        Tarea para realizar la descarga del video usando yt_dlp en un hilo separado.
        """
        try:
            ydl_opts = {
                'outtmpl': f'{path}/%(title)s.%(ext)s',
                'format': 'bestvideo+bestaudio/best',  
                'progress_hooks': [progress_hook]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            if not cancel_download.is_set():
                messagebox.showinfo("Éxito", "¡Video descargado con éxito!")
                update_status("¡Descarga completa!")
        except Exception as e:
            if cancel_download.is_set():
                update_status("Descarga cancelada.")
            else:
                messagebox.showerror("Error", f"Error al descargar el video: {e}")
                update_status("La descarga falló.")
            progress_var.set(0)  # Restablecer barra de progreso en caso de error

    # Ejecutar la tarea de descarga en un hilo separado
    threading.Thread(target=download_task).start()

def download_mp3():
    """
    Descarga el audio desde la URL proporcionada y lo convierte a formato MP3.
    """
    url = url_entry.get()
    path = download_path.get()  # Usa la ruta guardada
    
    if not url or not path:
        messagebox.showwarning("Error de entrada", "Por favor, proporcione una URL de video y una ruta de descarga.")
        return

    progress_var.set(0)  # Restablecer barra de progreso
    update_status("Iniciando descarga...")
    cancel_download.clear()  # Limpiar el evento de cancelación

    def download_task():
        """
        Tarea para realizar la descarga de audio y conversión a MP3 usando yt_dlp en un hilo separado.
        """
        try:
            def hook(d):
                """
                Función hook para manejar actualizaciones de progreso y verificar cancelación.
                
                Args:
                    d (dict): Diccionario que contiene la información del progreso.
                """
                if cancel_download.is_set():
                    raise Exception("Descarga cancelada")
                if d['status'] == 'downloading':
                    total_bytes = d.get('total_bytes', 0)
                    downloaded_bytes = d.get('downloaded_bytes', 0)
                    update_progress_bar(downloaded_bytes, total_bytes)
                    message = d.get('info_dict', {}).get('title', 'Descargando...')
                    update_status(message)
                elif d['status'] == 'finished':
                    update_status(f"Descarga finalizada: {d['filename']}")
                    progress_var.set(100)
                    root.update_idletasks()

            ydl_opts = {
                'outtmpl': f'{path}/%(title)s.%(ext)s',
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'progress_hooks': [hook]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            if not cancel_download.is_set():
                messagebox.showinfo("Éxito", "¡Audio descargado y convertido con éxito!")
                update_status("¡Descarga y conversión completada!")
        except Exception as e:
            if cancel_download.is_set():
                update_status("Descarga cancelada.")
            else:
                messagebox.showerror("Error", f"Error al descargar o convertir audio: {e}")
                update_status("La descarga o conversión falló.")
            progress_var.set(0)  # Restablecer barra de progreso en caso de error

    # Ejecutar la tarea de descarga en un hilo separado
    threading.Thread(target=download_task).start()

def set_download_path():
    """
    Abrir un diálogo para seleccionar una ruta de descarga y guardarla.
    """
    path = filedialog.askdirectory()
    if path:
        download_path.set(path)
        save_config({'download_path': path})

def cancel_operation():
    """
    Cancelar la descarga o conversión en curso.
    """
    cancel_download.set()
    update_status("Cancelando...")
    progress_var.set(0)

# Cargar configuración guardada
config = load_config()
initial_path = config.get('download_path', '')

# Crear la GUI
root = tk.Tk()
root.title("Andolon - Descargador de YouTube")

# Configurar color de fondo y tamaño de la ventana
root.configure(bg="#2C3E50")
root.geometry("450x460")

# Añadir estilos personalizados para etiquetas y botones
tk.Label(root, text="URL de YouTube:", bg="#2C3E50", fg="white", font=("Helvetica", 12, "bold")).pack(pady=10)

# Campo de entrada con padding y color de fondo
url_entry = tk.Entry(root, width=40, font=("Helvetica", 10), bg="#ECF0F1", fg="#2C3E50", bd=0)
url_entry.pack(pady=5, ipady=5)

# Variable de ruta de descarga
download_path = tk.StringVar(value=initial_path)

# Campo de entrada para la ruta de descarga con un botón para cambiarla
path_entry = tk.Entry(root, textvariable=download_path, width=40, font=("Helvetica", 10), bg="#ECF0F1", fg="#2C3E50", bd=0, state=tk.DISABLED)
path_entry.pack(pady=5, ipady=5)

# Botón para cambiar la ruta de descarga
change_path_button = tk.Button(root, text="Cambiar ruta de descarga", bg="#3498DB", fg="white", font=("Helvetica", 10, "bold"), relief="flat", padx=10, pady=5, command=set_download_path)
change_path_button.pack(pady=10)

# Botón estilizado para descargar video
download_button = tk.Button(root, text="Descargar Video", bg="#E74C3C", fg="white", font=("Helvetica", 10, "bold"), relief="flat", padx=20, pady=5, command=download_video)
download_button.pack(pady=5)

# Botón estilizado para descargar MP3
download_mp3_button = tk.Button(root, text="Descargar MP3", bg="#E67E22", fg="white", font=("Helvetica", 10, "bold"), relief="flat", padx=20, pady=5, command=download_mp3)
download_mp3_button.pack(pady=5)

# Cancel button
cancel_button = tk.Button(root, text="Cancelar Descarga", bg="#34495E", fg="white", font=("Helvetica", 10, "bold"), relief="flat", padx=20, pady=5, command=cancel_operation)
cancel_button.pack(pady=10)

# Barra de progreso
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(fill=tk.X, padx=10, pady=20)

# Etiqueta de estado
status_label = tk.Label(root, text="Listo", bg="#2C3E50", fg="white", font=("Helvetica", 10))
status_label.pack()

# Powered by label
powered_by_label = tk.Label(root, text="Powered by Andolon - GitHub Andolon-M", bg="#2C3E50", fg="white", font=("Helvetica", 8))
powered_by_label.pack(side=tk.BOTTOM, pady=5)


# Iniciar el bucle principal
root.mainloop()
