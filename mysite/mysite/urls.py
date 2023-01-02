from django.contrib import admin
from django.urls import path, include
from app.views import home_view, AnnounceCreate, AnnounceComment, register_code_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home_view, name='login'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls')),
    path('announce/', include('app.urls')),
    path('comments/', AnnounceComment.as_view()),
    path('announce_create/', AnnounceCreate.as_view()),
    path('register_code/', register_code_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
