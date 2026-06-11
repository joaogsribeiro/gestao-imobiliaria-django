from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from imoveis import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('accounts/', include('django.contrib.auth.urls')),

    # Público
    path('', views.home, name='home'),
    path('imovel/<int:pk>/', views.detalhe_imovel, name='detalhe_imovel'),

    # Usuário logado
    path('perfil/', views.perfil_cliente, name='perfil_cliente'),
    path('anunciar/', views.anunciar_imovel, name='anunciar_imovel'),

    # Admin — Imóveis
    path('imovel/novo/',             views.cadastrar_imovel,    name='cadastrar_imovel'),
    path('imovel/<int:pk>/editar/',  views.editar_imovel,       name='editar_imovel'),
    path('imovel/<int:pk>/deletar/', views.deletar_imovel,      name='deletar_imovel'),
    path('imoveis/pendentes/',       views.pendentes_aprovacao, name='pendentes_aprovacao'),
    path('imovel/<int:pk>/aprovar/', views.aprovar_imovel,      name='aprovar_imovel'),
    path('imovel/<int:pk>/rejeitar/',views.rejeitar_imovel,     name='rejeitar_imovel'),

    # Admin — Clientes
    path('clientes/',                  views.listar_clientes,  name='listar_clientes'),
    path('clientes/novo/',             views.cadastrar_cliente, name='cadastrar_cliente'),
    path('clientes/<int:pk>/editar/',  views.editar_cliente,   name='editar_cliente'),
    path('clientes/<int:pk>/deletar/', views.deletar_cliente,  name='deletar_cliente'),

    # Admin — Contratos
    path('contratos/',                  views.listar_contratos,  name='listar_contratos'),
    path('contratos/novo/',             views.cadastrar_contrato, name='cadastrar_contrato'),
    path('contratos/<int:pk>/editar/',  views.editar_contrato,   name='editar_contrato'),
    path('contratos/<int:pk>/deletar/', views.deletar_contrato,  name='deletar_contrato'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
