from django.shortcuts import render, get_object_or_404
from .models import Imovel


def home(request):
    imoveis = Imovel.objects.all()

    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    bairro = request.GET.get('bairro', '').strip()

    if q:
        imoveis = imoveis.filter(titulo__icontains=q) | \
                  imoveis.filter(bairro__icontains=q) | \
                  imoveis.filter(endereco__icontains=q)
    if status:
        imoveis = imoveis.filter(status=status)
    if bairro:
        imoveis = imoveis.filter(bairro__icontains=bairro)

    return render(request, 'imoveis/home.html', {'imoveis': imoveis})


def detalhe_imovel(request, pk):
    imovel = get_object_or_404(Imovel, pk=pk)
    return render(request, 'imoveis/detalhe.html', {'imovel': imovel})
