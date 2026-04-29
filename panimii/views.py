import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import ContactoForm

logger = logging.getLogger(__name__)


def contacto(request):
    """
    Vista de la página de contacto.

    GET  → muestra el formulario vacío.
    POST → valida; si es válido envía el correo vía SMTP y redirige
           (patrón PRG para evitar reenvíos al refrescar).
           Si el envío falla, muestra un error amigable sin exponer
           los detalles técnicos al usuario.
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
                    subject      = asunto,
                    message      = cuerpo,
                    from_email   = settings.DEFAULT_FROM_EMAIL,
                    recipient_list = [settings.EMAIL_DESTINATARIO],
                    fail_silently= False,
                )
                messages.success(
                    request,
                    '¡Mensaje enviado! Te contestaremos pronto. 🐻',
                )
            except Exception as exc:
                # Registra el error en el log del servidor sin exponerlo al usuario
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
