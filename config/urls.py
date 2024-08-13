from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mailing.urls', namespace='mailing')),
    path('users/', include('users.urls', namespace='users')),
    path('blogpost/', include('blogpost.urls', namespace='blogpost')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
