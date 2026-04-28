from django import forms


class ContactoForm(forms.Form):
    """
    Formulario de contacto / pedidos especiales.
    La validación se hace en Django; no usa modelos.
    """
    nombre = forms.CharField(
        max_length=100,
        label='Nombre completo',
        widget=forms.TextInput(attrs={
            'placeholder': 'Tu nombre',
            'id': 'id_nombre',
            'autocomplete': 'name',
        }),
        error_messages={'required': 'Por favor escribe tu nombre.'},
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'correo@ejemplo.com',
            'id': 'id_email',
            'autocomplete': 'email',
        }),
        error_messages={
            'required': 'Por favor escribe tu correo.',
            'invalid': 'Ingresa un correo válido.',
        },
    )
    mensaje = forms.CharField(
        label='Mensaje o pedido especial',
        widget=forms.Textarea(attrs={
            'placeholder': '¿Qué tienes en mente? Cuéntanos tu pedido, sabor favorito, fecha de entrega...',
            'rows': 6,
            'id': 'id_mensaje',
        }),
        error_messages={'required': 'Por favor escribe tu mensaje.'},
    )
