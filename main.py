from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Form, Path
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid
from operation import insert_data_audio, insert_data_watermark
from processing import add_watermark
from audio_extraction import extract_audio_from_video 

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) middleware to allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the path to the upload folder
upload_folder = "uploads"

# Create the upload folder if it doesn't exist
os.makedirs(upload_folder, exist_ok=True)

# Define the path to the audio folder
audio_folder = "audio"

# Create the audio folder if it doesn't exist
os.makedirs(audio_folder, exist_ok=True)

def generate_unique_filename(file_name: str) -> str:
    unique_identifier = str(uuid.uuid4())
    _, extension = os.path.splitext(file_name)
    return f"{unique_identifier}{extension}"

@app.post("/uploadforaudio/")
async def upload_and_process(file: UploadFile = File(...), uploaded_by: str = Form(...)):
    try:
        # Generate a unique filename for the uploaded file
        unique_filename = generate_unique_filename(file.filename)

        # Save the uploaded file to the upload folder with the unique filename
        file_path = os.path.join(upload_folder, unique_filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        try:
            insert_data_audio(unique_filename, uploaded_by, file_path)  # Assuming this function exists
            pass
        except Exception as e:
            print("Some error occurred while saving it in the database", e)

        # Process the audio and save to the audio folder with the unique filename
        audio_path = os.path.join(audio_folder, unique_filename.replace(".mp4", ".wav"))
        extract_audio_from_video(file_path, audio_path)

        return JSONResponse(content={"message": "File uploaded and processed successfully", "audio_path": audio_path}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"An error occurred: {str(e)}"}, status_code=500)

@app.get("/get_audio/{file_identifier}")
async def get_audio(file_identifier: str):
    try:
        # Construct the audio file path based on the unique identifier
        audio_path = os.path.join(audio_folder, file_identifier.replace(".mp4", ".wav"))

        # Check if the audio file exists
        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail="Audio file not found")

        # Return the audio file as a streaming response
        return StreamingResponse(open(audio_path, "rb"), media_type="application/octet-stream")
    except Exception as e:
        return JSONResponse(content={"message": f"An error occurred: {str(e)}"}, status_code=500)

UPLOADS_DIR = os.path.join("video_storage", "Uploads")

@app.post("/upload-video/")
async def upload_video(
    file: UploadFile = File(...),
    watermark_position: int = Query(..., description="Watermark position (1 to 8)"),
    username: str = Form(..., description="Username"),
):
    try:
        os.makedirs(UPLOADS_DIR, exist_ok=True)

        unique_id = str(uuid.uuid4())

        # Combine unique ID and sanitized filename
        filename = f"{unique_id}"

        file_path = os.path.join(UPLOADS_DIR, filename)

        print(file_path)

        file_path = file_path.replace("\\", "\\\\")

        with open(file_path, "wb") as video_file:
            shutil.copyfileobj(file.file, video_file)

        try:
            insert_data_watermark(unique_id, username)
            pass
        except Exception as e:
            print("Some error occurred while saving it in the database", e)

        # Apply watermark to the uploaded video
        add_watermark(unique_id, file_path, position_case=watermark_position)

        return JSONResponse(
            content={
                "message": "File uploaded successfully",
                "file_path": file_path,
                "watermark_position": watermark_position,
                "username": username,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


PROCESSED_DIR = os.path.join("video_storage", "Processed")

@app.get("/get-processed-video/{uid}")
async def get_processed_video(
    uid: str = Path(..., description="Unique ID of the video")
):
    try:
        processed_filename = f"{uid}.mp4"
        print(processed_filename)
        processed_filepath = os.path.join(PROCESSED_DIR, processed_filename)

        if not os.path.exists(processed_filepath):
            raise HTTPException(status_code=404, detail="Processed video not found")
        return StreamingResponse(
            open(processed_filepath, "rb"), media_type="application/octet-stream"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)