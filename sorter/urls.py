from django.urls import path, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/add_directory/', views.api_add_dir),
    path('api/get_images/', views.api_get_images),
    path('api/update_rates/', views.api_update_rates),
    path('api/get_image/', views.api_get_image),
    path('api/get_directories/', views.api_get_directories),
    path('api/update_directory/', views.api_update_directory)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
