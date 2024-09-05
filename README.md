# Andolon - YouTube Downloader

Andolon es una aplicación de escritorio que permite a los usuarios descargar videos de YouTube y convertirlos a formato MP3. Esta aplicación utiliza `yt_dlp` para manejar las descargas y la conversión de formatos, y `tkinter` para su interfaz gráfica.

## Índice

1. [Funcionamiento Interno](#funcionamiento-interno)
   - [Estructura del Código](#estructura-del-código)
   - [Diseño de la Interfaz](#diseño-de-la-interfaz)
2. [Instalación y Requisitos](#instalación-y-requisitos)
   - [Librerías Necesarias](#librerías-necesarias)
   - [Instalación de Dependencias](#instalación-de-dependencias)
   - [Archivos Adicionales](#archivos-adicionales)
3. [Uso del Usuario Final](#uso-del-usuario-final)
   - [Requisitos Adicionales](#requisitos-adicionales)
   - [Instrucciones para el Usuario](#instrucciones-para-el-usuario)
   - [Consejos Adicionales](#consejos-adicionales)

---

## Funcionamiento Interno

### Estructura del Código

1. **Configuración y Dependencias**
   - **Módulos Importados**:
     - `tkinter`: Para crear la interfaz gráfica de usuario (GUI).
     - `yt_dlp`: Para descargar videos y convertirlos a MP3.
     - `os`, `pickle`, `threading`: Para manejo de archivos de configuración y operaciones en segundo plano.

2. **Archivo de Configuración**
   - **`CONFIG_FILE`**: Archivo `config.pkl` para almacenar la ruta de descarga seleccionada por el usuario.
   - **Funciones**:
     - `load_config()`: Carga la configuración guardada (ruta de descarga).
     - `save_config(config)`: Guarda la configuración actual.

3. **Actualización de la Interfaz**
   - **`update_progress_bar(downloaded_bytes, total_bytes)`**: Actualiza la barra de progreso según la cantidad de bytes descargados.
   - **`update_status(message)`**: Actualiza la etiqueta de estado en la interfaz gráfica con el mensaje proporcionado.

4. **Descarga de Videos y Audios**
   - **`progress_hook(d)` y `hook(d)`**: Funciones para manejar las actualizaciones de progreso durante la descarga.
   - **`download_video()`**: Configura y ejecuta la descarga del video usando `yt_dlp` en un hilo separado.
   - **`download_mp3()`**: Configura y ejecuta la descarga y conversión a MP3 usando `yt_dlp` en un hilo separado.

5. **Manejo de la Operación**
   - **`set_download_path()`**: Abre un diálogo para seleccionar la ruta de descarga y la guarda en la configuración.
   - **`cancel_operation()`**: Cancela la operación de descarga en curso utilizando un `Event` de threading.

### Diseño de la Interfaz

- **Ventana Principal**: Configurada con `tkinter`, incluye campos para ingresar la URL del video, seleccionar la ruta de descarga, y botones para iniciar la descarga o la conversión a MP3.
- **Barra de Progreso y Etiqueta de Estado**: Muestran el progreso de la descarga y el estado actual.

## Instalación y Requisitos

### Librerías Necesarias

Para que la aplicación funcione correctamente, necesitas instalar las siguientes librerías:

- `yt_dlp`: Para manejar la descarga y conversión de videos.
- `tkinter`: Para la interfaz gráfica de usuario. (Generalmente viene preinstalada con Python, pero en algunos sistemas puede necesitar instalación adicional).

### Instalación de Dependencias

1. **Clonar el Repositorio**
   ```bash
   git clone https://github.com/Andolon-M/Descargador-de-videos-de-youtube.git
   cd tu_repositorio
   ```

2. **Instalar Dependencias**
   - **Para Windows, Mac, y Linux**: Asegúrate de tener Python instalado. Luego, instala las librerías necesarias con `pip`.
   ```bash
   pip install yt-dlp
   ```

   - **Instalación de `tkinter`**:
     - En la mayoría de los casos, `tkinter` se incluye con Python. Si encuentras problemas, puedes instalarlo usando:
       - **Windows**: Asegúrate de instalar Python con la opción para `Add Python to PATH`.
       - **Linux**: Instalar con el paquete del sistema. Por ejemplo, en Ubuntu:
         ```bash
         sudo apt-get install python3-tk
         ```

### Archivos Adicionales

Para la conversión a MP3, necesitas los siguientes archivos ejecutables en el mismo directorio donde se ejecuta el programa:

- `ffmpeg`
- `ffplay`
- `ffprobe`

Descarga estos archivos desde [FFmpeg](https://ffmpeg.org/download.html) y colócalos en la carpeta donde está el ejecutable de la aplicación.

## Uso del Usuario Final

### Requisitos Adicionales

Para que la conversión a MP3 funcione correctamente, debes asegurarte de que los archivos ejecutables `ffmpeg`, `ffplay`, y `ffprobe` estén disponibles en la misma carpeta donde se ejecuta el programa. Estos archivos son necesarios para procesar y convertir el audio a formato MP3. Puedes descargar estos archivos desde el sitio web de [FFmpeg](https://ffmpeg.org/download.html) y colocarlos en el directorio del ejecutable.

### Instrucciones para el Usuario

1. **Preparar el Entorno**
   - **Ubicación de Archivos FFmpeg**:
     - Descarga los archivos `ffmpeg`, `ffplay`, y `ffprobe` desde el sitio web de [FFmpeg](https://ffmpeg.org/download.html).
     - Coloca estos archivos en la misma carpeta donde se encuentra el ejecutable del programa.
   
2. **Ejecutar la Aplicación**
   - **Windows**: Haz doble clic en el archivo ejecutable `.exe`.
   - **Mac/Linux**: Abre una terminal y ejecuta el archivo usando `python nombre_del_archivo.py`.

3. **Interfaz de Usuario**
   - **URL de YouTube**:
     - Ingresa la URL del video o la lista de reproducción de YouTube que deseas descargar en el campo de texto "YouTube URL:".
     - Se admiten tanto videos individuales como listas de reproducción.
   
   - **Selección de Formato**:
     - **MP4**: Si deseas descargar el video en formato MP4, haz clic en el botón "Download Video".
     - **MP3**: Si prefieres extraer el audio y convertirlo a formato MP3, haz clic en el botón "Download MP3".

4. **Ruta de Descarga**:
   - **Modificar**: Haz clic en "Change Download Path" para seleccionar la carpeta donde se guardará el archivo descargado.
   - **Ver**: La ruta seleccionada se mostrará en el campo de texto bajo el botón.

5. **Opciones de Descarga**:
   - **Download Video**: Descarga el video en el mejor formato disponible (MP4 por defecto).
   - **Download MP3**: Descarga el audio del video y lo convierte a formato MP3 utilizando los archivos FFmpeg.
   
6. **Cancelar Operación**:
   - Si necesitas cancelar la descarga o conversión en curso, haz clic en el botón "Cancel Operation". La operación se detendrá y la barra de progreso se reiniciará.

7. **Monitoreo del Progreso**
   - **Barra de Progreso**: Muestra el avance de la descarga o conversión en porcentaje.
   - **Etiqueta de Estado**: Informa sobre el estado actual de la operación (iniciando, en progreso, completado, o error).

8. **Errores y Mensajes**
   - **Errores**: Si ocurre un error durante la descarga o conversión, se mostrará un mensaje de error en una ventana emergente.
   - **Éxito**: Cuando la descarga o conversión se complete con éxito, se mostrará un mensaje de éxito en una ventana emergente.

### Consejos Adicionales

- **Verifica que los archivos FFmpeg estén correctamente ubicados**: La conversión a MP3 no funcionará si estos archivos no están en el directorio del ejecutable.
- **Asegúrate de ingresar una URL válida**: La aplicación admite tanto videos individuales como listas de reproducción. Si introduces una lista de reproducción, todos los videos en la lista serán descargados.
- **Revisa la ruta de descarga** antes de iniciar la operación para asegurar que los archivos se guardarán en la ubicación deseada.

