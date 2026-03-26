import os
from fastapi import File, HTTPException, UploadFile
from fastapi import APIRouter
from fastapi import Depends
import aiofiles

from src.settings import Settings
from src.settings import settings
from src.upload.dependencies import get_upload_deps


upload_router = APIRouter(prefix=settings.UPLOAD_PREFIX)


@upload_router.post(settings.UPLOAD_ENDPOINT)
async def upload_image(file: UploadFile = File(...), settings: Settings = Depends(get_upload_deps)):
    """
    Receives an uploaded image file and saves it locally.
    """
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")

    file_location = os.path.join(settings.UPLOAD_DIR, file.filename)
    try:
        async with aiofiles.open(file_location, "wb") as buffer:
            while chunk := await file.read(1024):
                await buffer.write(chunk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error uploading the file: {e}")
    finally:
        await file.close()

    return {"message": f"Successfully uploaded {file.filename}", "location": file_location}
