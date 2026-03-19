import shutil

from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.services.image_service import ImageService
from src.tasks.tasks import resize_and_save_image


router = APIRouter(prefix="/images", tags=["Картинки к отелю"])


@router.post("")
def upload_images(file: UploadFile, background_tasks: BackgroundTasks):
    ImageService().resize_image(file=file, background_tasks=background_tasks)
