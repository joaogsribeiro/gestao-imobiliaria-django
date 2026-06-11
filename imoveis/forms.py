from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Imovel, Cliente, ContratoAluguel

W = {'class': 'form-control'}
S = {'class': 'form-select'}


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={**W, 'placeholder': 'seu@email.com'}),
        label='E-mail',
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({**W, 'placeholder': 'Seu usuário'})
        self.fields['username'].label = 'Usuário'
        self.fields['password1'].widget.attrs.update({**W, 'placeholder': 'Sua senha'})
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].widget.attrs.update({**W, 'placeholder': 'Confirme a senha'})
        self.fields['password2'].label = 'Confirmar senha'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


# ─── Admin forms ─────────────────────────────────────────────────────────────

class ImovelForm(forms.ModelForm):
    class Meta:
        model = Imovel
        fields = ['proprietario', 'titulo', 'endereco', 'bairro', 'valor_aluguel', 'status']
        widgets = {
            'proprietario': forms.Select(attrs=S),
            'titulo': forms.TextInput(attrs={**W, 'placeholder': 'Ex: Apartamento 2 quartos no Centro'}),
            'endereco': forms.TextInput(attrs={**W, 'placeholder': 'Rua, número, complemento'}),
            'bairro': forms.TextInput(attrs={**W, 'placeholder': 'Nome do bairro'}),
            'valor_aluguel': forms.NumberInput(attrs={**W, 'placeholder': '0.00', 'step': '0.01'}),
            'status': forms.Select(attrs=S),
        }
        labels = {
            'proprietario': 'Proprietário',
            'titulo': 'Título',
            'endereco': 'Endereço',
            'bairro': 'Bairro',
            'valor_aluguel': 'Valor do Aluguel (R$)',
            'status': 'Status',
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'telefone', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={**W, 'placeholder': 'Nome completo'}),
            'cpf': forms.TextInput(attrs={**W, 'placeholder': '000.000.000-00'}),
            'telefone': forms.TextInput(attrs={**W, 'placeholder': '(00) 00000-0000'}),
            'email': forms.EmailInput(attrs={**W, 'placeholder': 'email@exemplo.com'}),
        }
        labels = {'nome': 'Nome', 'cpf': 'CPF', 'telefone': 'Telefone', 'email': 'E-mail'}


class ContratoAluguelForm(forms.ModelForm):
    class Meta:
        model = ContratoAluguel
        fields = ['imovel', 'locatario', 'data_inicio', 'data_termino', 'valor_fechado']
        widgets = {
            'imovel': forms.Select(attrs=S),
            'locatario': forms.Select(attrs=S),
            'data_inicio': forms.DateInput(format='%Y-%m-%d', attrs={**W, 'type': 'date'}),
            'data_termino': forms.DateInput(format='%Y-%m-%d', attrs={**W, 'type': 'date'}),
            'valor_fechado': forms.NumberInput(attrs={**W, 'step': '0.01', 'placeholder': '0.00'}),
        }
        labels = {
            'imovel': 'Imóvel', 'locatario': 'Locatário',
            'data_inicio': 'Data de Início', 'data_termino': 'Data de Término',
            'valor_fechado': 'Valor Fechado (R$)',
        }


# ─── User/Client forms ────────────────────────────────────────────────────────

class RegistrarClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'telefone', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={**W, 'placeholder': 'Seu nome completo'}),
            'cpf': forms.TextInput(attrs={**W, 'placeholder': '000.000.000-00'}),
            'telefone': forms.TextInput(attrs={**W, 'placeholder': '(00) 00000-0000'}),
            'email': forms.EmailInput(attrs={**W, 'placeholder': 'email@exemplo.com'}),
        }
        labels = {'nome': 'Nome completo', 'cpf': 'CPF', 'telefone': 'Telefone', 'email': 'E-mail'}


class AnunciarImovelForm(forms.ModelForm):
    class Meta:
        model = Imovel
        fields = ['titulo', 'endereco', 'bairro', 'valor_aluguel']
        widgets = {
            'titulo': forms.TextInput(attrs={**W, 'placeholder': 'Ex: Apartamento 2 quartos no Centro'}),
            'endereco': forms.TextInput(attrs={**W, 'placeholder': 'Rua, número, complemento'}),
            'bairro': forms.TextInput(attrs={**W, 'placeholder': 'Nome do bairro'}),
            'valor_aluguel': forms.NumberInput(attrs={**W, 'placeholder': '0.00', 'step': '0.01'}),
        }
        labels = {
            'titulo': 'Título do anúncio',
            'endereco': 'Endereço',
            'bairro': 'Bairro',
            'valor_aluguel': 'Valor do aluguel (R$)',
        }
