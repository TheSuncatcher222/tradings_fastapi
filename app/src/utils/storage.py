"""
Вспомогательные функции по работе с файловым хранилищем.
"""

from io import BufferedReader
from mimetypes import guess_type
from os import remove as os_remove
from pathlib import Path
from shutil import rmtree


class LocalStorage:
    """
    Класс вспомогательных функций по работе с файловым хранилищем.
    """

    def delete_directory(
        self,
        *,
        path_str: str | None = None,
        path: Path | None = None,
        raise_exception: bool = False,
    ) -> None:
        """
        Удаляет директорию по указанному пути.
        """
        try:
            if path is None:
                if path_str is None:
                    raise OSError('Не указан путь до удаляемой директории.')
                path: Path = Path(path_str)

            if path.exists() and path.is_dir():
                rmtree(path)
            else:
                raise OSError(f'Директория {path} не существует.')

        except OSError:
            # TODO. Добавить логирование.
            if raise_exception:
                raise

        return

    def delete_files(
        self,
        *,
        paths: list[str],
        raise_exception: bool = False,
    ) -> None:
        """
        Удаляет файлы по указанным путям.
        """
        for path in paths:
            try:
                os_remove(path)
            except OSError:
                # TODO. Добавить логирование.
                if raise_exception:
                    raise
        return

    def read_file(
        self,
        *,
        path: str,
        raise_exception: bool = False,
    ) -> bytes | None:
        """
        Читает файл по указанному пути.
        """
        try:
            with open(path, 'rb') as file_obj:
                return file_obj.read()
        except FileNotFoundError:
            # TODO. Добавить логирование.
            if raise_exception:
                raise
            return None

    def write_file(
        self,
        *,
        path: str,
        data: bytes,
    ) -> None:
        """
        Записывает файл по указанному пути.
        """
        with open(path, 'wb') as file_obj:
            file_obj.write(data)
        return


local_storage: LocalStorage = LocalStorage()


def parse_file_info(
    file: BufferedReader,
) -> tuple[str, str, str]:
    """
    Парсит медиа-информацию о файле.
    """
    mime_type: str | None = guess_type(file.name)[0]
    if mime_type:
        maintype, subtype = mime_type.split('/')
    else:
        maintype, subtype = 'application', 'octet-stream'
    filename: str = file.name
    return filename, maintype, subtype
