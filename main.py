from fastapi import FastAPI, File, UploadFile
import os
import shutil

app = FastAPI()

# Create uploads folder if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    """Handle PDF file uploads"""
    # Construct the file path where the uploaded file will be saved
    file_path = f"uploads/{file.filename}"
    
    # Open the destination file in binary write mode and copy the uploaded file into it
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Return success response with filename and message
    return {
        "filename": file.filename,
        "message": "File uploaded successfully"
    }