from functools import wraps
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.urls import reverse
from .models import Imovel, ImagemImovel, Cliente, ContratoAluguel
from .forms import (
    ImovelForm, RegistroUsuarioForm, ClienteForm, ContratoAluguelForm,
    RegistrarClienteForm, AnunciarImovelForm,
)


# ─── Decorador de staff ───────────────────────────────────────────────────────

def staff_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{reverse('login')}?next={request.path}")
        if not request.user.is_staff:
            messages.error(request, 'Acesso restrito a administradores.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


# ─── Home (público) ───────────────────────────────────────────────────────────

def home(request):
    imoveis = Imovel.objects.filter(aprovacao='aprovado')
    total_imoveis = imoveis.count()

    q      = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    bairro = request.GET.get('bairro', '').strip()

    if q:
        imoveis = imoveis.filter(
            Q(titulo__icontains=q) | Q(bairro__icontains=q) | Q(endereco__icontains=q)
        )
    if status:
        imoveis = imoveis.filter(status=status)
    if bairro:
        imoveis = imoveis.filter(bairro__icontains=bairro)

    return render(request, 'imoveis/home.html', {'imoveis': imoveis, 'total_imoveis': total_imoveis})


def detalhe_imovel(request, pk):
    imovel = get_object_or_404(Imovel, pk=pk)
    if imovel.aprovacao != 'aprovado' and not request.user.is_staff:
        if imovel.submetido_por != request.user:
            messages.error(request, 'Este imóvel não está disponível.')
            return redirect('home')
    return render(request, 'imoveis/detalhe.html', {'imovel': imovel})


# ─── Autenticação ────────────────────────────────────────────────────────────

def cadastrar_usuario(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
            return redirect('login')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registration/cadastrar.html', {'form': form})


# ─── Perfil do usuário / Cadastro como cliente ───────────────────────────────

@login_required
def perfil_cliente(request):
    cliente = getattr(request.user, 'cliente', None)

    if request.method == 'POST':
        form = RegistrarClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            c = form.save(commit=False)
            c.usuario = request.user
            c.save()
            messages.success(request, 'Perfil atualizado!' if cliente else 'Você agora é um cliente!')
            return redirect('perfil_cliente')
    else:
        initial = {'nome': request.user.get_full_name() or request.user.username,
                   'email': request.user.email}
        form = RegistrarClienteForm(instance=cliente, initial=None if cliente else initial)

    imoveis_submetidos = Imovel.objects.filter(submetido_por=request.user).order_by('-pk') if cliente else []

    return render(request, 'perfil/perfil.html', {
        'form': form,
        'cliente': cliente,
        'imoveis_submetidos': imoveis_submetidos,
    })


# ─── Anunciar imóvel (usuário cliente) ───────────────────────────────────────

@login_required
def anunciar_imovel(request):
    cliente = getattr(request.user, 'cliente', None)
    if not cliente:
        messages.warning(request, 'Você precisa completar seu cadastro de cliente antes de anunciar.')
        return redirect('perfil_cliente')

    if request.method == 'POST':
        form = AnunciarImovelForm(request.POST, request.FILES)
        if form.is_valid():
            imovel = form.save(commit=False)
            imovel.proprietario  = cliente
            imovel.aprovacao     = 'pendente'
            imovel.submetido_por = request.user
            imovel.save()
            for imagem in request.FILES.getlist('imagens'):
                ImagemImovel.objects.create(imovel=imovel, imagem=imagem)
            messages.success(request, 'Imóvel enviado para aprovação! O administrador revisará em breve.')
            return redirect('perfil_cliente')
    else:
        form = AnunciarImovelForm()

    return render(request, 'imoveis/anunciar.html', {'form': form})


# ─── Aprovação (admin) ────────────────────────────────────────────────────────

@staff_required
def pendentes_aprovacao(request):
    pendentes  = Imovel.objects.filter(aprovacao='pendente').select_related('proprietario', 'submetido_por')
    rejeitados = Imovel.objects.filter(aprovacao='rejeitado').select_related('proprietario', 'submetido_por')
    return render(request, 'imoveis/pendentes.html', {'pendentes': pendentes, 'rejeitados': rejeitados})


@staff_required
def aprovar_imovel(request, pk):
    if request.method == 'POST':
        imovel = get_object_or_404(Imovel, pk=pk)
        imovel.aprovacao = 'aprovado'
        imovel.save()
        messages.success(request, f'Imóvel "{imovel.titulo}" aprovado e publicado.')
    return redirect('pendentes_aprovacao')


@staff_required
def rejeitar_imovel(request, pk):
    if request.method == 'POST':
        imovel = get_object_or_404(Imovel, pk=pk)
        imovel.aprovacao = 'rejeitado'
        imovel.save()
        messages.warning(request, f'Imóvel "{imovel.titulo}" rejeitado.')
    return redirect('pendentes_aprovacao')


# ─── CRUD de Imóveis (admin) ─────────────────────────────────────────────────

@staff_required
def cadastrar_imovel(request):
    if request.method == 'POST':
        form = ImovelForm(request.POST, request.FILES)
        if form.is_valid():
            imovel = form.save()
            for imagem in request.FILES.getlist('imagens'):
                ImagemImovel.objects.create(imovel=imovel, imagem=imagem)
            messages.success(request, 'Imóvel cadastrado com sucesso!')
            return redirect('detalhe_imovel', pk=imovel.pk)
    else:
        form = ImovelForm()
    return render(request, 'imoveis/form_imovel.html', {'form': form, 'titulo': 'Cadastrar Imóvel'})


@staff_required
def editar_imovel(request, pk):
    imovel = get_object_or_404(Imovel, pk=pk)
    if request.method == 'POST':
        form = ImovelForm(request.POST, request.FILES, instance=imovel)
        if form.is_valid():
            imovel = form.save()
            ids_deletar = request.POST.getlist('deletar_imagens')
            if ids_deletar:
                ImagemImovel.objects.filter(pk__in=ids_deletar, imovel=imovel).delete()
            for imagem in request.FILES.getlist('imagens'):
                ImagemImovel.objects.create(imovel=imovel, imagem=imagem)
            messages.success(request, 'Imóvel atualizado!')
            return redirect('detalhe_imovel', pk=imovel.pk)
    else:
        form = ImovelForm(instance=imovel)
    return render(request, 'imoveis/form_imovel.html', {
        'form': form, 'imovel': imovel,
        'titulo': 'Editar Imóvel', 'imagens': imovel.imagens.all(),
    })


@staff_required
def deletar_imovel(request, pk):
    imovel = get_object_or_404(Imovel, pk=pk)
    if request.method == 'POST':
        imovel.delete()
        messages.success(request, f'Imóvel "{imovel.titulo}" removido.')
        return redirect('home')
    return render(request, 'confirmar_exclusao.html', {
        'objeto': imovel, 'tipo': 'imóvel',
        'cancel_url': reverse('detalhe_imovel', args=[imovel.pk]),
    })


# ─── CRUD de Clientes (admin) ─────────────────────────────────────────────────

@staff_required
def listar_clientes(request):
    q = request.GET.get('q', '').strip()
    clientes = Cliente.objects.annotate(imoveis_count=Count('imoveis'))
    if q:
        clientes = clientes.filter(Q(nome__icontains=q) | Q(cpf__icontains=q) | Q(email__icontains=q))
    return render(request, 'clientes/listar.html', {'clientes': clientes, 'q': q})


@staff_required
def cadastrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.nome}" cadastrado!')
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/form_cliente.html', {'form': form, 'titulo': 'Cadastrar Cliente'})


@staff_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cliente "{cliente.nome}" atualizado!')
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/form_cliente.html', {
        'form': form, 'cliente': cliente, 'titulo': 'Editar Cliente',
    })


@staff_required
def deletar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, f'Cliente "{cliente.nome}" removido.')
        return redirect('listar_clientes')
    return render(request, 'confirmar_exclusao.html', {
        'objeto': cliente, 'tipo': 'cliente',
        'cancel_url': reverse('listar_clientes'),
    })


# ─── CRUD de Contratos (admin) ────────────────────────────────────────────────

@staff_required
def listar_contratos(request):
    contratos = ContratoAluguel.objects.select_related('imovel', 'locatario').all()
    return render(request, 'contratos/listar.html', {'contratos': contratos})


@staff_required
def cadastrar_contrato(request):
    if request.method == 'POST':
        form = ContratoAluguelForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Contrato criado com sucesso!')
                return redirect('listar_contratos')
            except Exception as e:
                messages.error(request, f'Erro ao salvar: {e}')
    else:
        form = ContratoAluguelForm()
    return render(request, 'contratos/form_contrato.html', {'form': form, 'titulo': 'Novo Contrato'})


@staff_required
def editar_contrato(request, pk):
    contrato = get_object_or_404(ContratoAluguel, pk=pk)
    if request.method == 'POST':
        form = ContratoAluguelForm(request.POST, instance=contrato)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contrato atualizado!')
            return redirect('listar_contratos')
    else:
        form = ContratoAluguelForm(instance=contrato)
    return render(request, 'contratos/form_contrato.html', {
        'form': form, 'contrato': contrato, 'titulo': 'Editar Contrato',
    })


@staff_required
def deletar_contrato(request, pk):
    contrato = get_object_or_404(ContratoAluguel, pk=pk)
    if request.method == 'POST':
        contrato.delete()
        messages.success(request, 'Contrato removido.')
        return redirect('listar_contratos')
    return render(request, 'confirmar_exclusao.html', {
        'objeto': contrato, 'tipo': 'contrato',
        'cancel_url': reverse('listar_contratos'),
    })
