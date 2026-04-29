from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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


class RegistroForm(UserCreationForm):
    """
    Formulario de registro público.

    Extiende UserCreationForm añadiendo el campo email (requerido)
    y traduciendo los labels/mensajes de error al español.
    """
    email = forms.EmailField(
        required=True,
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'correo@ejemplo.com',
            'autocomplete': 'email',
        }),
        error_messages={
            'required': 'Por favor ingresa tu correo.',
            'invalid':  'Ingresa un correo válido.',
        },
    )

    class Meta:
        model  = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Nombre de usuario',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'tu_usuario',
                'autocomplete': 'username',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Traducir placeholders y labels de los campos heredados
        self.fields['password1'].label   = 'Contraseña'
        self.fields['password2'].label   = 'Confirmar contraseña'
        self.fields['password1'].widget  = forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'autocomplete': 'new-password',
        })
        self.fields['password2'].widget  = forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'autocomplete': 'new-password',
        })
        # Quitar los textos de ayuda genéricos de Django
        for field in self.fields.values():
            field.help_text = ''

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
