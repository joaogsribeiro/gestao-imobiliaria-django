from .models import Imovel, Cliente


def user_context(request):
    ctx = {'user_cliente': None, 'pendentes_count': 0}
    if request.user.is_authenticated:
        try:
            ctx['user_cliente'] = request.user.cliente
        except Cliente.DoesNotExist:
            pass
        if request.user.is_staff:
            ctx['pendentes_count'] = Imovel.objects.filter(aprovacao='pendente').count()
    return ctx
