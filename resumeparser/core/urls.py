from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home),
    # path('gen/',views.genview,name="general"),
    path('final/',views.final),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)