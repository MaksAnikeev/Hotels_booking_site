import shutil

from fastapi import UploadFile, BackgroundTasks

from src.services.base_service import BaseService
from src.tasks.tasks import resize_and_save_image


class ImageService(BaseService):
    def resize_image(
        self, file: UploadFile, background_tasks: BackgroundTasks
    ) -> None:

        image_path = f"src/static/images/{file.filename}"
        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)

            # тоже самое что селери, но для легких задач, не забудь убрать декоратор с таски
            # background_tasks.add_task(resize_and_save_image, image_path)
            resize_and_save_image.delay(image_path)
