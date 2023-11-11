# Video Processing Webservice

## Setup

### Step 1

Download the FFmpeg build folder from the given link [https://github.com/BtbN/FFmpeg-Builds/releases](https://github.com/BtbN/FFmpeg-Builds/releases). From the `bin` folder, copy `ffmpeg.exe` and `ffprobe.exe` into your project directory.

### Step 2

Set up a Python virtual environment using the command:  
```python -m venv <virtualenviourmentname>```

### Step 3
go inside the python evnviourment by using:  
```<virtualenviourmentname>/Scripts/activate```

### Step 4
install all the python libraries in your virtual enviourment by using:  
```pip install -r requirements.txt```

### Step 5
Now run the server by using:  
```uvicorn main:app```

## Testing
All testing can be done on fastapi swagger UI by going to the URL https://localhost:8000/docs  

### Video upload For Audio Extraction API
![/uploadforaudio](screenshots\audio_upload.jpg?raw=true)

### Audio download API
![/getaudio/{file_identifier}](screenshots\audio_download.jpg?raw=true)

### Video upload for Watermarking API
![/upload-video](screenshots\video_upload.jpg?raw=true)

### Watermarked video download API
![/get-processed-video/{uid}](screenshots\video_watermark_download.jpg?raw=true)

