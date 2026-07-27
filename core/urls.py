from django.urls import include, path
from rest_framework.routers import DefaultRouter

# Importamos las vistas
from .views import *

router = DefaultRouter()

router.register("biography", BiographyViewSet, basename="biography")
router.register("technologies", TechnologyViewSet, basename="technology")
router.register("projects", ProjectViewSet, basename="project")
router.register("experience", ExperienceViewSet, basename="experience")
router.register("education", EducationViewSet, basename="education")
router.register("social-links", SocialLinkViewSet, basename="social-link")

urlpatterns = [
    path("portfolio/", PortfolioAPIView.as_view(), name="portfolio"),
    path("contact/", ContactAPIView.as_view(), name="Contact"),
    path("", include(router.urls)),
]