from fastapi import APIRouter, UploadFile, BackgroundTasks
from src.services.image_service import ImageService

router = APIRouter(prefix="/images", tags=["Картинки к отелю"])


@router.post("")
async def upload_images(file: UploadFile, background_tasks: BackgroundTasks):
    image_path = ImageService().resize_image(
        file=file, background_tasks=background_tasks
    )
    return {
        "status": "OK",
        "filename": file.filename,
        "saved_path": image_path,
    }
