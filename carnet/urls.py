from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from contacts import views


urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('', include('contacts.urls')),  # Accès aux URLs de l'app contacts
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='contacts/login.html'), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
