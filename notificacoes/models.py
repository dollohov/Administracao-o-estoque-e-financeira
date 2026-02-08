from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Notificacao(models.Model):
    """
    Modelo que representa uma notificação do sistema.
    
    As notificações são criadas automaticamente quando eventos importantes ocorrem
    (estoque crítico, novo pedido, etc).
    """
    
    TIPO_CHOICES = (
        ('ESTOQUE', 'Alerta de Estoque'),
        ('PEDIDO', 'Novo Pedido'),
        ('FINANCEIRO', 'Alerta Financeiro'),
        ('SISTEMA', 'Notificação do Sistema'),
        ('VENDA', 'Alerta de Venda'),
    )
    
    PRIORIDADE_CHOICES = (
        ('BAIXA', 'Baixa'),
        ('MEDIA', 'Média'),
        ('ALTA', 'Alta'),
        ('URGENTE', 'Urgente'),
    )
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notificacoes',
        verbose_name="Usuário"
    )
    
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name="Tipo de Notificação"
    )
    
    prioridade = models.CharField(
        max_length=10,
        choices=PRIORIDADE_CHOICES,
        default='MEDIA',
        verbose_name="Prioridade"
    )
    
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título"
    )
    
    mensagem = models.TextField(
        verbose_name="Mensagem"
    )
    
    lida = models.BooleanField(
        default=False,
        verbose_name="Lida"
    )
    
    url_acao = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="URL da Ação",
        help_text="URL para onde o usuário será redirecionado ao clicar na notificação"
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    
    data_leitura = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Data de Leitura"
    )
    
    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        ordering = ['-data_criacao']
        indexes = [
            models.Index(fields=['usuario', '-data_criacao']),
            models.Index(fields=['usuario', 'lida']),
        ]
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"
    
    def marcar_como_lida(self):
        """Marca a notificação como lida."""
        if not self.lida:
            self.lida = True
            self.data_leitura = timezone.now()
            self.save()
    
    @property
    def cor_prioridade(self):
        """Retorna a cor Bootstrap correspondente à prioridade."""
        cores = {
            'BAIXA': 'info',
            'MEDIA': 'warning',
            'ALTA': 'danger',
            'URGENTE': 'danger',
        }
        return cores.get(self.prioridade, 'secondary')
