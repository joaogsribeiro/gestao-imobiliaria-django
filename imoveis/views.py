from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Imovel


def home(request):
    imoveis = Imovel.objects.all()

    q = request.GET.get('q', '').strip()
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

    return render(request, 'imoveis/home.html', {'imoveis': imoveis})


def detalhe_imovel(request, pk):
    imovel = get_object_or_404(Imovel, pk=pk)
    return render(request, 'imoveis/detalhe.html', {'imovel': imovel})
