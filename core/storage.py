import mimetypes
import uuid

from django.core.files.storage import Storage

from .services.supabase_storage import get_storage_service


class SupabaseStorage(Storage):
    """
    Storage personalizado para Supabase Storage.
    """

    def __init__(self):
        self.service = get_storage_service()

    def _save(self, name, content):
        """
        Guarda un archivo en Supabase.
        """

        extension = ""

        if "." in name:
            extension = "." + name.split(".")[-1]

        filename = f"{uuid.uuid4().hex}{extension}"

        if "/" in name:
            folder = name.rsplit("/", 1)[0]
            path = f"{folder}/{filename}"
        else:
            path = filename

        content.seek(0)

        data = content.read()

        content_type = (
            getattr(content, "content_type", None)
            or mimetypes.guess_type(name)[0]
            or "application/octet-stream"
        )

        self.service.upload_file(
            path=path,
            content=data,
            content_type=content_type,
        )

        return path

    def delete(self, name):
        """
        Elimina un archivo.
        """

        if name:
            self.service.delete_file(name)

    def exists(self, name):
        """
        Comprueba si existe.
        """

        return self.service.exists(name)

    def url(self, name):
        """
        Devuelve la URL pública.
        """

        return self.service.get_public_url(name)

    def size(self, name):
        """
        Django no necesita este dato para nuestro proyecto.
        """

        return 0

    def get_accessed_time(self, name):
        return None

    def get_created_time(self, name):
        return None

    def get_modified_time(self, name):
        return None
