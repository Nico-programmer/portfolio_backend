from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.db.models import FileField

from .models import (
    Biography,
    Technology,
    Project,
    ProjectImage,
    Experience,
    Education,
)


MODELS = [
    Biography,
    Technology,
    Project,
    ProjectImage,
    Experience,
    Education,
]


def get_file_fields(instance):
    """
    Retorna todos los FileField/ImageField del modelo.
    """
    return [
        field
        for field in instance._meta.get_fields()
        if isinstance(field, FileField)
    ]


for model in MODELS:

    @receiver(pre_save, sender=model)
    def delete_old_files(sender, instance, **kwargs):
        if not instance.pk:
            return

        try:
            old_instance = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return

        for field in get_file_fields(instance):

            old_file = getattr(old_instance, field.name)
            new_file = getattr(instance, field.name)

            if (
                old_file
                and old_file.name
                and old_file != new_file
            ):
                old_file.delete(save=False)


    @receiver(post_delete, sender=model)
    def delete_files(sender, instance, **kwargs):

        for field in get_file_fields(instance):

            file = getattr(instance, field.name)

            if file:
                file.delete(save=False)