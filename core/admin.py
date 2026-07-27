from django.contrib import admin
from django.utils.html import format_html

from .models import *


# ======================================================================================================================
# Función para previsualizar imágenes
# ======================================================================================================================

def image_preview(image, width=80):
    if image:
        return format_html(
            '<img src="{}" width="{}" style="border-radius:8px; object-fit:cover;" />',
            image.url,
            width,
        )
    return "-"


# ======================================================================================================================
# Biografía
# ======================================================================================================================

@admin.register(Biography)
class BiographyAdmin(admin.ModelAdmin):
    list_display = (
        "profile_preview",
        "full_name",
        "profession",
        "available_for_work",
        "updated_at",
    )

    list_filter = (
        "available_for_work",
    )

    search_fields = (
        "full_name",
        "profession",
    )

    readonly_fields = (
        "profile_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Información Personal",
            {
                "fields": (
                    "full_name",
                    "profession",
                    "short_description",
                    "about",
                )
            },
        ),
        (
            "Archivos",
            {
                "fields": (
                    "profile_picture",
                    "profile_preview",
                    "cv",
                )
            },
        ),
        (
            "Configuración",
            {
                "fields": (
                    "available_for_work",
                )
            },
        ),
        (
            "Fechas del Sistema",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    @admin.display(description="Foto")
    def profile_preview(self, obj):
        return image_preview(obj.profile_picture)


# ======================================================================================================================
# Tecnologías
# ======================================================================================================================

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = (
        "icon_preview",
        "name",
        "category",
        "level",
        "order",
        "is_visible",
    )

    list_editable = (
        "order",
        "is_visible",
    )

    list_filter = (
        "category",
        "is_visible",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "order",
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    readonly_fields = (
        "icon_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Información General",
            {
                "fields": (
                    "name",
                    "slug",
                    "category",
                    "level",
                )
            },
        ),
        (
            "Icono",
            {
                "fields": (
                    "icon",
                    "icon_preview",
                )
            },
        ),
        (
            "Configuración",
            {
                "fields": (
                    "order",
                    "is_visible",
                )
            },
        ),
        (
            "Fechas del Sistema",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    @admin.display(description="Ícono")
    def icon_preview(self, obj):
        return image_preview(obj.icon, 40)


# ======================================================================================================================
# Proyectos
# ======================================================================================================================

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "thumbnail_preview",
        "title",
        "status",
        "featured",
        "order",
        "is_visible",
    )

    list_editable = (
        "featured",
        "order",
        "is_visible",
    )

    list_filter = (
        "status",
        "featured",
        "is_visible",
    )

    search_fields = (
        "title",
        "description",
    )

    ordering = (
        "order",
        "-created_at",
    )

    filter_horizontal = (
        "technologies",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    readonly_fields = (
        "thumbnail_preview",
        "created_at",
        "updated_at",
    )

    inlines = [
        ProjectImageInline,
    ]

    fieldsets = (
        (
            "Información General",
            {
                "fields": (
                    "title",
                    "slug",
                    "short_description",
                    "description",
                )
            },
        ),
        (
            "Imagen Principal",
            {
                "fields": (
                    "thumbnail",
                    "thumbnail_preview",
                )
            },
        ),
        (
            "Tecnologías",
            {
                "fields": (
                    "technologies",
                )
            },
        ),
        (
            "Enlaces",
            {
                "fields": (
                    "github_url",
                    "demo_url",
                )
            },
        ),
        (
            "Configuración",
            {
                "fields": (
                    "status",
                    "featured",
                    "order",
                    "is_visible",
                )
            },
        ),
        (
            "Fechas del Sistema",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    @admin.display(description="Miniatura")
    def thumbnail_preview(self, obj):
        return image_preview(obj.thumbnail, 90)


# ======================================================================================================================
# Imágenes de Proyecto
# ======================================================================================================================

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "image_preview",
        "order",
    )

    list_editable = (
        "order",
    )

    ordering = (
        "project",
        "order",
    )

    @admin.display(description="Imagen")
    def image_preview(self, obj):
        return image_preview(obj.image, 90)


# ======================================================================================================================
# Experiencia Laboral
# ======================================================================================================================

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "logo_preview",
        "company",
        "position",
        "current_job",
        "start_date",
        "end_date",
        "is_visible",
    )

    list_editable = (
        "is_visible",
    )

    list_filter = (
        "current_job",
        "is_visible",
    )

    search_fields = (
        "company",
        "position",
    )

    filter_horizontal = (
        "technologies",
    )

    readonly_fields = (
        "logo_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Información Laboral",
            {
                "fields": (
                    "company",
                    "position",
                    "description",
                )
            },
        ),
        (
            "Empresa",
            {
                "fields": (
                    "company_logo",
                    "logo_preview",
                    "location",
                )
            },
        ),
        (
            "Fechas",
            {
                "fields": (
                    "start_date",
                    "end_date",
                    "current_job",
                )
            },
        ),
        (
            "Tecnologías",
            {
                "fields": (
                    "technologies",
                )
            },
        ),
        (
            "Configuración",
            {
                "fields": (
                    "order",
                    "is_visible",
                )
            },
        ),
        (
            "Fechas del Sistema",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    @admin.display(description="Logo")
    def logo_preview(self, obj):
        return image_preview(obj.company_logo)


# ======================================================================================================================
# Educación
# ======================================================================================================================

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = (
        "logo_preview",
        "institution",
        "degree",
        "currently_studying",
        "start_date",
        "end_date",
    )

    list_editable = ()

    list_filter = (
        "currently_studying",
        "is_visible",
    )

    search_fields = (
        "institution",
        "degree",
    )

    readonly_fields = (
        "logo_preview",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Información Académica",
            {
                "fields": (
                    "institution",
                    "degree",
                    "description",
                )
            },
        ),
        (
            "Institución",
            {
                "fields": (
                    "institution_logo",
                    "logo_preview",
                )
            },
        ),
        (
            "Fechas",
            {
                "fields": (
                    "start_date",
                    "end_date",
                    "currently_studying",
                )
            },
        ),
        (
            "Certificado",
            {
                "fields": (
                    "certificate_url",
                )
            },
        ),
        (
            "Configuración",
            {
                "fields": (
                    "order",
                    "is_visible",
                )
            },
        ),
        (
            "Fechas del Sistema",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    @admin.display(description="Logo")
    def logo_preview(self, obj):
        return image_preview(obj.institution_logo)


# ======================================================================================================================
# Redes Sociales
# ======================================================================================================================

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "url",
        "order",
        "is_visible",
    )

    list_editable = (
        "order",
        "is_visible",
    )

    list_filter = (
        "is_visible",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "order",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Información",
            {
                "fields": (
                    "name",
                    "icon",
                    "url",
                )
            },
        ),
        (
            "Configuración",
            {
                "fields": (
                    "order",
                    "is_visible",
                )
            },
        ),
        (
            "Fechas del Sistema",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )