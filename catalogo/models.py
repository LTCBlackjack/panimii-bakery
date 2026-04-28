import os
from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from django.utils.text import slugify
from PIL import Image


class Categoria(models.Model):
    """Modelo para las categorías del catálogo de la panadería."""

    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0, help_text='Orden de aparición en el catálogo')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class Producto(models.Model):
    """
    Modelo para los productos de la panadería.

    Las imágenes subidas se comprimen automáticamente y se convierten
    a formato WebP para optimizar el almacenamiento del servidor (1 GB).
    """

    # ── Configuración de compresión ──────────────────────────────
    WEBP_QUALITY = 80           # Calidad WebP (0-100)
    MAX_IMAGE_SIZE = (1200, 1200)  # Dimensión máxima en píxeles

    # ── Campos del modelo ────────────────────────────────────────
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='productos',
    )
    imagen = models.ImageField(
        upload_to='productos/',
        blank=True,
        null=True,
        help_text='La imagen se comprimirá y convertirá a WebP automáticamente.',
    )
    disponible = models.BooleanField(default=True)
    destacado = models.BooleanField(
        default=False,
        help_text='Mostrar en la sección de productos destacados.',
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-destacado', '-creado']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['categoria', 'disponible']),
        ]

    def __str__(self):
        return self.nombre

    # ── Compresión automática de imágenes ────────────────────────
    def _compress_image(self):
        """
        Comprime la imagen subida y la convierte a formato WebP.

        - Redimensiona si excede MAX_IMAGE_SIZE (manteniendo proporción).
        - Convierte cualquier formato (PNG, JPEG, etc.) a WebP.
        - Aplica la calidad definida en WEBP_QUALITY.
        """
        if not self.imagen:
            return

        img = Image.open(self.imagen)

        # Convertir modos incompatibles con WebP (ej. CMYK, P, LA)
        if img.mode in ('RGBA', 'LA'):
            # Conservar transparencia
            pass
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # Redimensionar si excede las dimensiones máximas
        img.thumbnail(self.MAX_IMAGE_SIZE, Image.LANCZOS)

        # Guardar en buffer como WebP
        buffer = BytesIO()
        img.save(buffer, format='WEBP', quality=self.WEBP_QUALITY, optimize=True)
        buffer.seek(0)

        # Generar nuevo nombre con extensión .webp
        nombre_original = os.path.splitext(os.path.basename(self.imagen.name))[0]
        nuevo_nombre = f'{nombre_original}.webp'

        # Reemplazar el archivo de imagen
        self.imagen.save(nuevo_nombre, ContentFile(buffer.read()), save=False)

    def save(self, *args, **kwargs):
        # Generar slug automático si no existe
        if not self.slug:
            self.slug = slugify(self.nombre)

        # Comprimir imagen solo si es nueva o fue actualizada
        if self.pk:
            try:
                viejo = Producto.objects.get(pk=self.pk)
                imagen_cambio = viejo.imagen != self.imagen
            except Producto.DoesNotExist:
                imagen_cambio = True
        else:
            imagen_cambio = True

        # Primero guardamos para obtener el PK y la ruta del archivo
        super().save(*args, **kwargs)

        # Comprimir y re-guardar solo si la imagen cambió
        if imagen_cambio and self.imagen:
            self._compress_image()
            # Guardar de nuevo para persistir la imagen comprimida
            # Usamos update_fields para evitar recursión infinita
            super().save(update_fields=['imagen'])
