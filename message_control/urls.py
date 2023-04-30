from rest_framework.routers import DefaultRouter
from .views import GenerivFileUploadView
from django.urls import path, include

router = DefaultRouter(trailing_slash=False)

router.register("file-upload", GenerivFileUploadView)

urlpatterns = [
    path("", include(router.urls))
]
