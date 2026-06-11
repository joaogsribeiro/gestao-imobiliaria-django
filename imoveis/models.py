from django.db import models, transaction
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Cliente(models.Model):
    usuario = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cliente'
    )
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nome


class Imovel(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('alugado', 'Alugado'),
        ('manutencao', 'Em Manutenção'),
    ]
    APROVACAO_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    ]

    proprietario   = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='imoveis')
    titulo         = models.CharField(max_length=200)
    endereco       = models.CharField(max_length=255)
    bairro         = models.CharField(max_length=100)
    valor_aluguel  = models.DecimalField(max_digits=10, decimal_places=2)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')
    aprovacao      = models.CharField(max_length=20, choices=APROVACAO_CHOICES, default='aprovado')
    submetido_por  = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='imoveis_submetidos'
    )

    class Meta:
        verbose_name = 'Imóvel'
        verbose_name_plural = 'Imóveis'

    def __str__(self):
        return f"{self.titulo} - {self.bairro}"


class ImagemImovel(models.Model):
    imovel  = models.ForeignKey(Imovel, on_delete=models.CASCADE, related_name='imagens')
    imagem  = models.ImageField(upload_to='imoveis/')
    legenda = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Imagem do Imóvel'
        verbose_name_plural = 'Imagens dos Imóveis'

    def __str__(self):
        return f"Imagem de {self.imovel.titulo}"


class ContratoAluguel(models.Model):
    imovel        = models.ForeignKey(Imovel, on_delete=models.PROTECT, related_name='contratos')
    locatario     = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='contratos')
    data_inicio   = models.DateField()
    data_termino  = models.DateField()
    valor_fechado = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Contrato de Aluguel'
        verbose_name_plural = 'Contratos de Aluguel'

    def clean(self):
        if self.data_inicio and self.data_termino:
            if self.data_termino <= self.data_inicio:
                raise ValidationError({'data_termino': 'A data de término deve ser posterior à data de início.'})
        if not self.pk and self.imovel and self.imovel.status != 'disponivel':
            raise ValidationError({'imovel': 'Este imóvel não está disponível para um novo contrato.'})

    def save(self, *args, **kwargs):
        is_new = not self.pk
        with transaction.atomic():
            super().save(*args, **kwargs)
            if is_new:
                self.imovel.status = 'alugado'
                self.imovel.save(update_fields=['status'])

    def __str__(self):
        return f"Contrato: {self.imovel.titulo} - {self.locatario.nome}"