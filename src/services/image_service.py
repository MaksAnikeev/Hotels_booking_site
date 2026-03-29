import shutil
import re

from fastapi import UploadFile, BackgroundTasks
from pathlib import Path

from src.services.base_service import BaseService
from src.tasks.tasks import resize_and_save_image


class ImageService(BaseService):
    UPLOAD_DIR = Path(__file__).parent.parent / "static" / "images"

    def _sanitize_filename(self, filename: str) -> str:
        """
        Очищает имя файла от опасных символов, сохраняет юникод.
        """
        # 1. Берём только имя файла (без пути)
        name = Path(filename)

        # 2. Разделяем имя и расширение
        stem, ext = name.stem, name.suffix

        # 3. 🔥 Убираем опасные символы из имени (оставляем буквы, цифры, -, _, пробелы, юникод)
        # Разрешаем: буквы (включая кириллицу), цифры, пробелы, -, _
        safe_stem = re.sub(
            r"[^\w\s\-\u0400-\u04FF]", "_", stem
        )  # \u0400-\u04FF = кириллица

        # 4. Заменяем множественные пробелы/подчёркивания на один
        safe_stem = re.sub(r"[\s_]+", "_", safe_stem).strip("_")

        # 5. Обрезаем если слишком длинное (макс. 200 символов для имени + расширение)
        max_len = 200 - len(ext)
        safe_stem = safe_stem[:max_len]

        return f"{safe_stem}{ext}"

    def _get_unique_path(self, base_path: Path) -> Path:
        """
        Если файл с таким именем уже есть — добавляет счётчик: фото_1.png, фото_2.png...
        """
        if not base_path.exists():
            return base_path

        stem = base_path.stem
        ext = base_path.suffix
        counter = 1

        while True:
            new_path = base_path.parent / f"{stem}_{counter}{ext}"
            if not new_path.exists():
                return new_path
            counter += 1

    def resize_image(self, file: UploadFile, background_tasks: BackgroundTasks) -> str:

        # 1. Создаём папку
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        # 2. Очищаем и нормализуем имя файла
        safe_filename = self._sanitize_filename(file.filename)

        # 3. Полный путь к файлу
        base_path = self.UPLOAD_DIR / safe_filename

        # 4. Делаем имя уникальным (если файл уже есть)
        image_path = self._get_unique_path(base_path)

        # 5. Сохраняем файл
        with open(image_path, "wb") as new_file:
            shutil.copyfileobj(file.file, new_file)

        # 6. Отправляем задачу на ресайз
        resize_and_save_image.delay(str(image_path))

        return str(image_path)
