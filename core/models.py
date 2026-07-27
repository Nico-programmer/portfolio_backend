from django.db import models

# Biografia
class Biography(models.Model):
    full_name = models.CharField(max_length=150, verbose_name="Nombre Completo")
    profession = models.CharField(max_length=150, verbose_name="Profesión")
    short_description = models.CharField(max_length=150, verbose_name="Descripción Corta")
    about = models.TextField(verbose_name="Acerca de")
    profile_picture = models.ImageField(upload_to="biography/", verbose_name="Foto de perfil")
    cv = models.FileField(upload_to="cv/", verbose_name="Hoja de vida")
    available_for_work = models.BooleanField(default=True, verbose_name="Disponible para Trabajo")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        verbose_name = "Biografía"
        verbose_name_plural = "Biografías"
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Tecnologias
class Technology(models.Model):
    CATEGORY_CHOICES = (
        ("language", "Lenguaje"),
        ("frontend", "Frontend"),
        ("backend", "Backend"),
        ("database", "Base de datos"),
        ("devops", "DevOps"),
        ("tool", "Herramienta"),
    )

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="language", verbose_name="Categoría")
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Tecnología")
    slug = models.SlugField(max_length=120, unique=True, verbose_name="Slug")
    icon = models.ImageField(upload_to="technologies/", blank=True, null=True, verbose_name="icono")
    level = models.PositiveSmallIntegerField(default=3, verbose_name="Nivel")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")
    is_visible = models.BooleanField(default=True, verbose_name="¿Es Visible?")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        verbose_name = "Tecnología"
        verbose_name_plural = "Tecnologías"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Proyectos
class Project(models.Model):
    STATUS_CHOICES = (
        ("completed", "Completado"),
        ("in_progress", "En progreso"),
        ("archived", "Archivado"),
    )

    title = models.CharField(max_length=200, unique=True, verbose_name="Título del Proyecto")
    slug = models.SlugField(max_length=220, unique=True, verbose_name="Slug")
    short_description = models.CharField(max_length=200, verbose_name="Descripción Corta")
    description = models.TextField(verbose_name="Descripción")
    thumbnail = models.ImageField(upload_to="projects/thumbnails/", blank=True, null=True, verbose_name="Miniatura")
    technologies = models.ManyToManyField(Technology, related_name='projects', verbose_name="Tecnologías")
    github_url = models.URLField(blank=True, null=True, verbose_name="Repositorio de Github")
    demo_url = models.URLField(blank=True, null=True, verbose_name="Demo")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Progress', verbose_name="Estado")
    featured = models.BooleanField(default=False, verbose_name="Destacado")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")
    is_visible = models.BooleanField(default=True, verbose_name="¿Es Visible?")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

# Imagenes del proyecto
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_images", verbose_name="Proyecto")

    image = models.ImageField(upload_to="projects/gallery/", verbose_name="Imagen")
    alt_text = models.CharField(max_length=200, blank=True, null=True, verbose_name="Texto Alternativo")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")

    class Meta:
        verbose_name = "Imagen del Proyecto"
        verbose_name_plural = "Imágenes de los Proyectos"
        ordering = ["order"]

    def __str__(self):
        return f"{self.project.title} ({self.order})"

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Experiencia Laboral
class Experience(models.Model):
    company = models.CharField(max_length=150, verbose_name="Empresa")
    position = models.CharField(max_length=150, verbose_name="Cargo")
    description = models.TextField(verbose_name="Descripción")

    company_logo = models.ImageField(upload_to="experience/", blank=True, null=True, verbose_name="Logo de la Empresa")
    location = models.CharField(max_length=150, blank=True, null=True, verbose_name="Ubicación")

    start_date = models.DateField(verbose_name="Fecha de Inicio")
    end_date = models.DateField(blank=True, null=True, verbose_name="Fecha de Fin")

    current_job = models.BooleanField(default=False, verbose_name="¿Trabajo Actual?")

    technologies = models.ManyToManyField(Technology, related_name='experiences', blank=True, verbose_name="Tecnologías")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")

    is_visible = models.BooleanField(default=True, verbose_name="¿Es Visible?")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        verbose_name = "Experiencia Laboral"
        verbose_name_plural = "Experiencias Laborales"
        ordering = ['order', '-start_date']

    def __str__(self):
        return f"{self.position} en {self.company}"

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Redes Sociales
class SocialLink(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Red Social")
    icon = models.CharField(max_length=100, verbose_name="Ícono de la Red Social")

    url = models.URLField(verbose_name="URL de la Red Social")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")
    is_visible = models.BooleanField(default=True, verbose_name="¿Es Visible?")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        verbose_name = "Red Social"
        verbose_name_plural = "Redes Sociales"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Educación
class Education(models.Model):
    institution = models.CharField(max_length=150, verbose_name="Institución")
    degree = models.CharField(max_length=200, verbose_name="Título o programa")
    description = models.TextField(blank=True, verbose_name="Descripción")
    institution_logo = models.ImageField(upload_to="education/", verbose_name="Logo de la institución")

    start_date = models.DateField(verbose_name="Fecha de Inicio")
    end_date = models.DateField(blank=True, null=True, verbose_name="Fecha de Fin")

    currently_studying = models.BooleanField(default=False, verbose_name="¿Cursa actualmente?")
    certificate_url = models.URLField(blank=True, verbose_name="Certificado")

    order = models.PositiveIntegerField(default=0, verbose_name="Orden")
    is_visible = models.BooleanField(default=True, verbose_name="¿Es Visible?")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado el")

    class Meta:
        verbose_name = "Educación"
        verbose_name_plural = "Educación"
        ordering = ["order", "-start_date"]

    def __str__(self):
        return f"{self.degree} - {self.institution}"