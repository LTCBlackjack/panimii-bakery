import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.core.mail import send_mail
from django.shortcuts import redirect, render

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
