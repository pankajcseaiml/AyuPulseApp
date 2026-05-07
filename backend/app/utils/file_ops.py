"""
File operations utilities.
"""
import os
import shutil
from fastapi import UploadFile
from app.core.config import settings

UPLOAD_DIR = settings.UPLOAD_DIR

async def save_uploaded_file(upload_file: UploadFile, subdir: str) -> str:
    """
    Save an uploaded file to the uploads directory.
    Returns the relative path to the saved file.
    """
    # Validate file extension based on subdirectory
    ext = os.path.splitext(upload_file.filename)[1].lower()
    if subdir == "xray":
        allowed_extensions = settings.ALLOWED_IMAGE_EXTENSIONS
        file_type = "X-ray image"
    elif subdir == "ecg":
        allowed_extensions = settings.ALLOWED_ECG_EXTENSIONS
        file_type = "ECG data"
    else:
        allowed_extensions = settings.ALLOWED_IMAGE_EXTENSIONS + settings.ALLOWED_ECG_EXTENSIONS
        file_type = "file"
    
    if ext not in allowed_extensions:
        raise ValueError(f"{file_type} file extension {ext} not allowed. Allowed extensions for {subdir}: {allowed_extensions}")
    
    # Validate file size (max size in bytes)
    max_size = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    # Check content-length header if available (FastAPI provides it)
    if hasattr(upload_file, 'size') and upload_file.size:
        if upload_file.size > max_size:
            raise ValueError(f"File size ({upload_file.size / (1024*1024):.2f} MB) exceeds maximum of {settings.MAX_UPLOAD_SIZE_MB} MB")
    # We'll also check during streaming as a safety measure
    
    # Ensure uploads directory exists
    upload_path = os.path.join(UPLOAD_DIR, subdir)
    os.makedirs(upload_path, exist_ok=True)
    
    # Generate a safe filename
    import uuid
    if not ext:
        ext = ".bin"
    safe_filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(upload_path, safe_filename)
    
    # Write file with size checking
    total_size = 0
    with open(file_path, "wb") as buffer:
        while True:
            chunk = await upload_file.read(8192)
            if not chunk:
                break
            total_size += len(chunk)
            if total_size > max_size:
                buffer.close()
                os.remove(file_path)
                raise ValueError(f"File exceeds maximum size of {settings.MAX_UPLOAD_SIZE_MB} MB")
            buffer.write(chunk)
    
    # Return relative path
    return os.path.join(subdir, safe_filename)

async def delete_file(file_path: str) -> bool:
    """
    Delete a file from the uploads directory.
    """
    full_path = os.path.join(UPLOAD_DIR, file_path)
    if os.path.exists(full_path):
        os.remove(full_path)
        return True
    return False

def get_file_path(relative_path: str) -> str:
    """
    Get absolute file path from relative path.
    """
    return os.path.join(UPLOAD_DIR, relative_path)