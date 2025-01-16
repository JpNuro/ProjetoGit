from django import forms
from .models import Fruta

class FrutaForm(forms.ModelForm):
    class Meta:
        model = Fruta
        fields = ['nome', 'preco', 'quantidade', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
