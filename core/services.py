import logging

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


def send_contact_email(
    *,
    name: str,
    email: str,
    subject: str,
    message: str,
) -> bool:
    """
    Envía un correo con la información recibida desde el formulario de contacto.

    Returns:
        bool: True si el correo fue enviado correctamente, False en caso contrario.
    """

    email_subject = "📩 Nuevo mensaje desde tu Portafolio"

    email_body = f"""
        Hola Nicolás.

        Has recibido un nuevo mensaje desde tu portafolio.

        ──────────────────────────────

        Nombre:
        {name}

        Correo:
        {email}

        Asunto:
        {subject}

        ──────────────────────────────

        Mensaje:

        {message}

        ──────────────────────────────

        Este correo fue enviado automáticamente desde tu portafolio.
    """

    email_message = EmailMessage(
        subject=email_subject,
        body=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CONTACT_EMAIL],
        reply_to=[email],
    )

    try:
        email_message.send(fail_silently=False)

        logger.info(
            "Correo de contacto enviado correctamente desde %s.",
            email,
        )

        return True

    except Exception:
        logger.exception(
            "Error enviando correo de contacto desde %s.",
            email,
        )

        return False