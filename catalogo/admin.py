from django.contrib import admin

from .models import Categoria, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activa', 'orden', 'creado')
    list_editable = ('activa', 'orden')
    list_filter = ('activa',)
    search_fields = ('nombre',)
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'disponible', 'destacado', 'creado')
    list_editable = ('precio', 'disponible', 'destacado')
    list_filter = ('categoria', 'disponible', 'destacado')
    search_fields = ('nombre', 'descripcion')
    prepopulated_fields = {'slug': ('nombre',)}
    raw_id_fields = ('categoria',)
