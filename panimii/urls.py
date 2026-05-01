"""
URL configuration for panimii project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView

from . import views as project_views

urlpatterns = [
    # ── Páginas principales ──────────────────────────────────────
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('catalogo/', include('catalogo.urls', namespace='catalogo')),
    path('contacto/', project_views.contacto, name='contacto'),
    path('mi-cuenta/', project_views.dashboard, name='dashboard'),

    # ── Carrito ──────────────────────────────────────────────────────────
    path('carrito/', project_views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', project_views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/actualizar/<int:producto_id>/', project_views.actualizar_carrito, name='actualizar_carrito'),


    # ── Autenticación ────────────────────────────────────────────
    path('auth/login/', auth_views.LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True,
    ), name='login'),

    path('auth/logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('auth/registro/', project_views.registro, name='registro'),

    # ── Admin ────────────────────────────────────────────────────
    path('admin/', admin.site.urls),
]

# Servir archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
