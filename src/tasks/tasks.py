import asyncio
import datetime
import logging
import os
from typing import Union

from PIL import Image
from pathlib import Path


from src.database import async_session_factory_null_pull
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager


@celery_instance.task
def resize_and_save_image(image_path: Union[str, Path]) -> None:
    logging.debug(f"Запуск таски resize_and_save_image в celery по пути:{image_path=}")
    output_dir = "src/static/images"
    # Размеры по большей стороне
    sizes = [i for i in range(1000, 2000, 300)]

    # Преобразуем пути в Path-объекты для удобства
    image_path = Path(image_path)
    output_dir = Path(output_dir)

    # Проверяем, что файл существует
    if not image_path.is_file():
        raise FileNotFoundError(f"Файл не найден: {image_path}")

    # Создаём папку, если её нет
    output_dir.mkdir(parents=True, exist_ok=True)
    logging.info("Начинаем изменять размеры")
    # Открываем изображение
    with Image.open(image_path) as img:
        # Получаем имя файла без расширения
        base_name = image_path.stem
        ext = image_path.suffix.lower()  # .jpg, .png и т.д.

        for size in sizes:
            # Вычисляем новые размеры, сохраняя пропорции
            img_width, img_height = img.size
            ratio = min(size / img_width, size / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)

            # Изменяем размер
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Формируем имя файла
            new_file_name = f"{base_name}_{size}px{ext}"
            output_path = os.path.join(output_dir, new_file_name)

            # Сохраняем
            resized_img.save(output_path, quality=85, optimize=True)

        logging.info(
            f"Изображение сохранено в следующих размерах: {sizes} в папке {output_dir}"
        )


async def session_get_booking_chek_in_now():
    async with DBManager(session_factory=async_session_factory_null_pull) as db:
        bookings = await db.booking.get_booking_chek_in_now()
        logging.info(f"{bookings=}")


@celery_instance.task(name="booking_chek_in_today")
def send_email_to_user_checkin_today():
    asyncio.run(session_get_booking_chek_in_now())
