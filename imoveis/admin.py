from django.contrib import admin

# Register your models here.

from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Cliente, Imovel, ImagemImovel, ContratoAluguel

# Requisito: Implementação de Inlines
class ImagemImovelInline(TabularInline):
    model = ImagemImovel
    extra = 1  # Quantidade de campos em branco para novas fotos

@admin.register(Cliente)
class ClienteAdmin(ModelAdmin):
    list_display = ('nome', 'cpf', 'telefone', 'email')
    search_fields = ('nome', 'cpf', 'email')

@admin.register(Imovel)
class ImovelAdmin(ModelAdmin):
    # Requisito: list_display
    list_display = ('titulo', 'bairro', 'valor_aluguel', 'status')
    
    # Requisito: list_filter e search_fields
    list_filter = ('status', 'bairro')
    search_fields = ('titulo', 'endereco', 'bairro')
    
    # Requisito: Conectando o inline ao modelo principal
    inlines = [ImagemImovelInline]

@admin.register(ContratoAluguel)
class ContratoAluguelAdmin(ModelAdmin):
    list_display = ('imovel', 'locatario', 'data_inicio', 'data_termino', 'valor_fechado')
    list_filter = ('data_inicio', 'data_termino')
    search_fields = ('imovel__titulo', 'locatario__nome', 'locatario__cpf')