from django import forms

from .models import RegistroVenta, RedNeuronalResultados, Servicio

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin

class DateInput(forms.DateInput):
    input_type = 'date'

class RegistroVentaForm(forms.ModelForm):
    
    class Meta:
        model = RegistroVenta
        fields = '__all__'
        widgets = {
            'fecha': DateInput(),
        }

class ServicioForm(forms.ModelForm):
    
    class Meta:
        model = Servicio
        fields = '__all__'

class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin,
                             UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class EntrenarRedForm(forms.ModelForm):
    
    class Meta:
        model = RedNeuronalResultados
        fields = ['clasificacion', 'periodo', 'look_back', 'neuronas', 'epocas']