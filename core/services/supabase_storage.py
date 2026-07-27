from functools import lru_cache
from pathlib import PurePosixPath

from django.conf import settings
from supabase import Client, create_client


class SupabaseStorageService:
    """
    Servicio encargado de interactuar con Supabase Storage.
    """

    def __init__(self):
        self.client = get_supabase_client()
        self.bucket = settings.SUPABASE_BUCKET

    def upload_file(self, path: str, content: bytes, content_type: str | None = None):
        """
        Sube un archivo al bucket.
        """

        options = {
            "upsert": False,
        }

        if content_type:
            options["content-type"] = content_type

        return (
            self.client.storage
            .from_(self.bucket)
            .upload(
                path=path,
                file=content,
                file_options=options,
            )
        )

    def delete_file(self, path: str):
        """
        Elimina un archivo del bucket.
        """

        if not path:
            return

        return (
            self.client.storage
            .from_(self.bucket)
            .remove([path])
        )

    def get_public_url(self, path: str) -> str:
        """
        Devuelve la URL pública del archivo.
        """

        if not path:
            return ""

        return (
            self.client.storage
            .from_(self.bucket)
            .get_public_url(path)
        )

    def exists(self, path: str) -> bool:
        """
        Comprueba si existe un archivo.
        """

        try:
            folder = str(PurePosixPath(path).parent)

            response = (
                self.client.storage
                .from_(self.bucket)
                .list(folder)
            )

            filename = PurePosixPath(path).name

            return any(
                item["name"] == filename
                for item in response
            )

        except Exception:
            return False


@lru_cache(maxsize=1)
def get_supabase_client() -> Client:
    """
    Crea una única instancia del cliente de Supabase.
    """

    return create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_KEY,
    )


@lru_cache(maxsize=1)
def get_storage_service() -> SupabaseStorageService:
    """
    Devuelve una única instancia del servicio.
    """

    return SupabaseStorageService()