from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.upload_view, name='upload'),
<<<<<<< HEAD
     path('success/', views.upload_success, name='upload_success'),  # Add this line
=======
    path('success/', views.upload_success, name='upload_success'),  # Add this line
>>>>>>> 30eb68f792b1202acaea9330862ef28fc4904c44
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)