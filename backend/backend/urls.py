"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from web import views

    

urlpatterns = [
    path('admin/', admin.site.urls),
    path('web/login/', views.registro_usuario, name='registro_usuario'),
    path('web/inicio_sesion/', views.logear_users, name='logear_users'),
    path('web/administracion/', views.registro_usuariow, name='registro_usuariow'),
    path('web/cargar-usuarios/', views.cargar_usuarios, name='cargar_usuarios'),
    path('web/actualizar-usuario/', views.actualizar_usuario, name='actualizar_usuario'),
    path('web/eliminar-usuario/', views.eliminar_usuario, name='eliminar_usuario'),
    path('web/EsVIP/', views.verificar_vip, name='VIP'),
    path('web/cargar-mangas/', views.cargar_mangas, name='cargar_mangas'),
    path('web/mangas/', views.create_manga, name='crear_manga'),
    path('web/eliminar-manga/', views.eliminar_manga, name='eliminar_manga'),
    path('web/obtener-mangas/', views.obtener_mangas, name='obtener_mangas')
]
