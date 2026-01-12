"""
URL configuration for project_2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .views import serve_media


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('user/', include('user_domain.user_auth.urls')),
    path('user/member', include('user_domain.user_member.urls')),
    path('user/trainer', include('user_domain.user_trainer.urls')),
    path('org/', include('org_domain.org_auth.urls')),
    path('org/members', include("org_domain.members.urls")),
    path('org/payment', include("org_domain.payments.urls")),
    path("org/trainers", include("org_domain.trainers.urls")),
    path("media/<path:path>", serve_media),
] 
