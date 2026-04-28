from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactoForm


def contacto(request):
    """
    Vista de la página de contacto.

    GET  → muestra el formulario vacío.
    POST → valida; si es válido muestra mensaje de éxito y redirige,
           si no, devuelve el formulario con errores.
    """
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # TODO: aquí se enviará el email (SMTP / SendGrid) cuando
            # se configure el servidor de producción.
            messages.success(
                request,
                '¡Mensaje recibido! Te contactaremos pronto. 🐻',
            )
            return redirect('contacto')
    else:
        form = ContactoForm()

    return render(request, 'contacto.html', {'form': form})
