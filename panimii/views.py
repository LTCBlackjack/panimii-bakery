import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from catalogo.models import Producto
from .forms import ContactoForm, RegistroForm

logger = logging.getLogger(__name__)


def contacto(request):
    """
    GET  → formulario vacío.
    POST → envía correo SMTP y redirige (PRG).
    """
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            nombre  = form.cleaned_data['nombre']
            email   = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']

            asunto = f'[Paniimi Bakery] Nuevo mensaje de {nombre}'
            cuerpo = (
                f'Nombre:  {nombre}\n'
                f'Correo:  {email}\n'
                f'\n'
                f'Mensaje:\n{mensaje}\n'
                f'\n'
                f'--- Enviado desde el formulario de contacto de Paniimi Bakery ---'
            )

            try:
                send_mail(
                    subject        = asunto,
                    message        = cuerpo,
                    from_email     = settings.DEFAULT_FROM_EMAIL,
                    recipient_list = [settings.EMAIL_DESTINATARIO],
                    fail_silently  = False,
                )
                messages.success(request, '¡Mensaje enviado! Te contestaremos pronto. 🐻')
            except Exception as exc:
                logger.error('Error al enviar correo de contacto: %s', exc)
                messages.error(
                    request,
                    'Hubo un problema al enviar tu mensaje. '
                    'Intenta de nuevo o escríbenos directamente a contacto@paniimi.com.',
                )

            return redirect('contacto')
    else:
        form = ContactoForm()

    return render(request, 'contacto.html', {'form': form})


def registro(request):
    """
    Vista de registro público.

    GET  → formulario vacío.
    POST → crea el usuario, lo autentica automáticamente y redirige al inicio.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}! Tu cuenta fue creada.')
            return redirect('home')
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})


# ════════════════════════════════════════════════════════════════════════
# CARRITO DE COMPRAS  (sesión — sin modelo por ahora)
# Estructura de session['carrito']:
#   { 'producto_id': { nombre, precio, cantidad, imagen } }
# ════════════════════════════════════════════════════════════════════════

def ver_carrito(request):
    """
    Construye la lista de ítems del carrito desde la sesión
    y calcula totales para pasarlos al template.
    """
    from decimal import Decimal, InvalidOperation

    carrito_session = request.session.get('carrito', {})
    items  = []
    total  = Decimal('0.00')

    for producto_id, datos in carrito_session.items():
        try:
            precio   = Decimal(str(datos['precio']))
            cantidad = int(datos['cantidad'])
            subtotal = precio * cantidad
            items.append({
                'id':       producto_id,
                'nombre':   datos['nombre'],
                'precio':   precio,
                'cantidad': cantidad,
                'imagen':   datos.get('imagen', ''),
                'subtotal': subtotal,
            })
            total += subtotal
        except (InvalidOperation, KeyError, ValueError):
            continue  # omite entradas corruptas

    return render(request, 'carrito.html', {
        'items': items,
        'total': total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    })


def agregar_al_carrito(request, producto_id):
    """
    POST: añade 1 unidad del producto al carrito de sesión.
    Redirige a la página anterior (Referer) o al catálogo.
    """
    from catalogo.models import Producto as ProductoModel
    if request.method != 'POST':
        return redirect('catalogo:lista')

    try:
        producto = ProductoModel.objects.get(id=producto_id, disponible=True)
    except ProductoModel.DoesNotExist:
        messages.error(request, 'Producto no disponible.')
        return redirect('catalogo:lista')

    carrito   = request.session.get('carrito', {})
    key       = str(producto_id)

    if key in carrito:
        carrito[key]['cantidad'] += 1
    else:
        carrito[key] = {
            'nombre':   producto.nombre,
            'precio':   str(producto.precio),
            'cantidad': 1,
            'imagen':   producto.imagen.url if producto.imagen else '',
        }

    request.session['carrito']  = carrito
    request.session.modified    = True

    messages.success(request, f'"{producto.nombre}" añadido al carrito.')
    return redirect(request.META.get('HTTP_REFERER', 'catalogo:lista'))


def actualizar_carrito(request, producto_id):
    """
    POST: incrementa (+), decrementa (-) o elimina un ítem del carrito.
    Requiere campo 'accion' = 'mas' | 'menos' | 'eliminar'.
    """
    if request.method != 'POST':
        return redirect('ver_carrito')

    accion  = request.POST.get('accion', '')
    carrito = request.session.get('carrito', {})
    key     = str(producto_id)

    if key in carrito:
        if accion == 'mas':
            carrito[key]['cantidad'] += 1
        elif accion == 'menos':
            if carrito[key]['cantidad'] > 1:
                carrito[key]['cantidad'] -= 1
            else:
                del carrito[key]
        elif accion == 'eliminar':
            del carrito[key]

    request.session['carrito'] = carrito
    request.session.modified   = True
    return redirect('ver_carrito')



@login_required
def dashboard(request):
    """
    Panel principal del usuario autenticado.

    Muestra información de perfil, puntos de lealtad (placeholder),
    historial de pedidos (empty state por ahora) y productos sugeridos
    del catálogo real.
    """
    # Productos destacados o los 4 más recientes para "Sugeridos para ti"
    sugeridos = (
        Producto.objects
        .filter(disponible=True)
        .select_related('categoria')
        .order_by('-destacado', '-creado')[:4]
    )

    ctx = {
        'sugeridos':     sugeridos,
        'puntos_lealtad': 0,       # TODO: vincular a modelo Lealtad en Fase 3
        'pedidos':        [],      # TODO: vincular a modelo Pedido en Fase 3
    }
    return render(request, 'dashboard.html', ctx)
