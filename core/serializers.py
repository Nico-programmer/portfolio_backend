from rest_framework import serializers

# Modelos
from .models import *

# Biografia
class BiographySerializer(serializers.ModelSerializer):
    class Meta:
        model = Biography
        fields = "__all__"

# Tecnologias
class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = "__all__"

# Proyectos (Imagen y información)
class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ("id", "image", "alt_text", "order", )

class ProjectSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(
        many=True,
        read_only=True,
    )

    images = ProjectImageSerializer(
        source="project_images",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Project
        fields = "__all__"

# Experiencia laboral
class ExperienceSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Experience
        fields = "__all__"

# Educación
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"

# Social Link
class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = "__all__"

# Contacto
class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=100,
        trim_whitespace=True
    )

    email = serializers.EmailField()

    subject = serializers.CharField(
        max_length=150,
        trim_whitespace=True
    )

    message = serializers.CharField()

    honeypot = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True
    )

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "El nombre es obligatorio."
            )

        return value

    def validate_subject(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "El asunto es obligatorio."
            )

        return value

    def validate_message(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "El mensaje es obligatorio."
            )

        if len(value) < 20:
            raise serializers.ValidationError(
                "El mensaje debe contener al menos 20 caracteres."
            )

        return value

    def validate_honeypot(self, value):
        if value:
            raise serializers.ValidationError(
                "Solicitud inválida."
            )

        return value

# Serializador general
class PortfolioSerializer(serializers.Serializer):
    biography = BiographySerializer()
    technologies = TechnologySerializer(many=True)
    projects = ProjectSerializer(many=True)
    experiences = ExperienceSerializer(many=True)
    education = EducationSerializer(many=True)
    social_links = SocialLinkSerializer(many=True)