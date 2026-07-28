import logging

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from django.conf import settings

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

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = settings.BREVO_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

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

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        sender={
            "name": "Portafolio",
            "email": settings.DEFAULT_FROM_EMAIL,
        },
        to=[
            {
                "email": settings.CONTACT_EMAIL,
            }
        ],
        reply_to={
            "email": email,
            "name": name,
        },
        subject=email_subject,
        text_content=email_body,
    )

    try:
        api_instance.send_transac_email(send_smtp_email)

        logger.info(
            "Correo de contacto enviado correctamente desde %s.",
            email,
        )

        return True

    except ApiException:
        logger.exception(
            "Error enviando correo de contacto desde %s.",
            email,
        )

        return False

    except Exception:
        logger.exception(
            "Error inesperado enviando correo de contacto desde %s.",
            email,
        )

        return False