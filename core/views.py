from django.shortcuts import render

# Importamos lo que requerimos de DRF
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle

# Importamos los modelos
from .models import *

# Importamos los serializadores
from .serializers import *

# Importamos el servicio
from .services import send_contact_email

# Biografia
class BiographyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Biography.objects.all()
    serializer_class = BiographySerializer

# Tecnologias
class TechnologyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Technology.objects.filter(is_visible=True).order_by("order", "name")
    serializer_class = TechnologySerializer

# Proyectos
class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.filter(is_visible=True).prefetch_related("technologies", "images").order_by("order")
    serializer_class = ProjectSerializer

# Experiencia laboral
class ExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Experience.objects.filter(is_visible=True).prefetch_related("technologies").order_by("order")
    serializer_class = ExperienceSerializer

# Educación
class EducationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Education.objects.filter(is_visible=True).order_by("order")
    serializer_class = EducationSerializer

# Social Link
class SocialLinkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SocialLink.objects.filter(is_visible=True).order_by("order")
    serializer_class = SocialLinkSerializer

# Contacto
class ContactAPIView(APIView):
    """
    Endpoint para recibir los mensajes enviados desde
    el formulario de contacto del portafolio.
    """

    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    serializer_class = ContactSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data.copy()

        # El honeypot solo se utiliza para validar bots.
        data.pop("honeypot", None)

        email_sent = send_contact_email(**data)

        if email_sent:
            return Response(
                {
                    "success": True,
                    "message": "Mensaje enviado correctamente.",
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "success": False,
                "message": "No fue posible enviar el mensaje.",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

# Vista general del proyecto
class PortfolioAPIView(APIView):
    def get(self, request):
        biography = Biography.objects.first()
        technologies = Technology.objects.filter(is_visible=True).order_by("order", "name")
        projects = Project.objects.filter(is_visible=True).prefetch_related("technologies", "project_images").order_by("order")
        experiences = Experience.objects.filter(is_visible=True).prefetch_related("technologies").order_by("order")
        education = Education.objects.filter(is_visible=True).order_by("order")
        social_links = SocialLink.objects.filter(is_visible=True).order_by("order")
        serializer = PortfolioSerializer(
            {
                "biography": biography,
                "technologies": technologies,
                "projects": projects,
                "experiences": experiences,
                "education": education,
                "social_links": social_links,
            }
        )

        return Response(serializer.data)