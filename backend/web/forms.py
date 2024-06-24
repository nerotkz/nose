from django import forms
from .models import MangaNuevo

class MangaForm(forms.ModelForm):
    class Meta:
        model = MangaNuevo
        fields = ('nombre', 'precio', 'imagen')