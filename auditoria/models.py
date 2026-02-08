"""
Modelos de Auditoria para rastreamento de acessos e alteracoes de dados.

Este modulo implementa um sistema de auditoria que registra:
- Quem acessou quais dados sensíveis (LGPD)
- Quem alterou quais registros
- Quando foram feitas as alteracoes
- Qual foi o valor anterior e o novo valor

Autor: Manus AI
Data: 2026-02-07
"""

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
import json


class LogAuditoria(models.Model):
    """
    Modelo para registrar todas as alteracoes em registros do sistema.
    
    Attributes:
        usuario: Usuario que realizou a acao
        tipo_acao: CRIAR, ATUALIZAR, DELETAR, VISUALIZAR
        content_type: Tipo de modelo alterado
        object_id: ID do objeto alterado
        objeto: Referencia generica para o objeto
        valores_anteriores: JSON com valores antes da alteracao
        valores_novos: JSON com valores apos a alteracao
        descricao: Descricao textual da acao
        endereco_ip: Endereco IP da requisicao
        user_agent: User-Agent do navegador
        data_hora: Data e hora da acao
    """
    
    TIPO_ACAO_CHOICES = [
        ('CRIAR', 'Criacao'),
        ('ATUALIZAR', 'Atualizacao'),
        ('DELETAR', 'Delecao'),
        ('VISUALIZAR', 'Visualizacao'),
        ('EXPORTAR', 'Exportacao'),
        ('ANONIMIZAR', 'Anonimizacao'),
    ]
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='acoes_auditoria',
        verbose_name='Usuario'
    )
    
    tipo_acao = models.CharField(
        max_length=20,
        choices=TIPO_ACAO_CHOICES,
        verbose_name='Tipo de Acao'
    )
    
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='Tipo de Modelo'
    )
    
    object_id = models.PositiveIntegerField(
        verbose_name='ID do Objeto'
    )
    
    objeto = GenericForeignKey('content_type', 'object_id')
    
    valores_anteriores = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Valores Anteriores',
        help_text='JSON com os valores antes da alteracao'
    )
    
    valores_novos = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Valores Novos',
        help_text='JSON com os valores apos a alteracao'
    )
    
    descricao = models.TextField(
        blank=True,
        verbose_name='Descricao da Acao'
    )
    
    endereco_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='Endereco IP'
    )
    
    user_agent = models.TextField(
        blank=True,
        verbose_name='User-Agent do Navegador'
    )
    
    data_hora = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data e Hora'
    )
    
    class Meta:
        verbose_name = 'Log de Auditoria'
        verbose_name_plural = 'Logs de Auditoria'
        ordering = ['-data_hora']
        indexes = [
            models.Index(fields=['usuario', '-data_hora']),
            models.Index(fields=['tipo_acao', '-data_hora']),
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        return f"{self.usuario} - {self.tipo_acao} - {self.content_type} #{self.object_id} - {self.data_hora.strftime('%d/%m/%Y %H:%M:%S')}"
    
    def get_mudancas(self):
        """Retorna um dicionario com as mudancas de cada campo."""
        if not self.valores_anteriores or not self.valores_novos:
            return {}
        
        mudancas = {}
        for campo, valor_novo in self.valores_novos.items():
            valor_anterior = self.valores_anteriores.get(campo)
            if valor_anterior != valor_novo:
                mudancas[campo] = {
                    'anterior': valor_anterior,
                    'novo': valor_novo
                }
        
        return mudancas


class LogAcessoDadosSensiveis(models.Model):
    """
    Modelo para registrar acessos a dados pessoais sensíveis (LGPD).
    
    Attributes:
        usuario: Usuario que acessou os dados
        tipo_dado: CPF, EMAIL, TELEFONE, ENDERECO, etc
        cliente_id: ID do cliente cujos dados foram acessados
        cliente_nome: Nome do cliente (para auditoria)
        motivo: Motivo do acesso
        endereco_ip: Endereco IP da requisicao
        user_agent: User-Agent do navegador
        data_hora: Data e hora do acesso
    """
    
    TIPO_DADO_CHOICES = [
        ('CPF', 'CPF/CNPJ'),
        ('EMAIL', 'Email'),
        ('TELEFONE', 'Telefone'),
        ('ENDERECO', 'Endereco'),
        ('DADOS_COMPLETOS', 'Todos os Dados Pessoais'),
        ('HISTORICO_VENDAS', 'Historico de Vendas'),
        ('HISTORICO_PAGAMENTOS', 'Historico de Pagamentos'),
    ]
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='acessos_dados_sensiveis',
        verbose_name='Usuario'
    )
    
    tipo_dado = models.CharField(
        max_length=50,
        choices=TIPO_DADO_CHOICES,
        verbose_name='Tipo de Dado Acessado'
    )
    
    cliente_id = models.PositiveIntegerField(
        verbose_name='ID do Cliente'
    )
    
    cliente_nome = models.CharField(
        max_length=255,
        verbose_name='Nome do Cliente'
    )
    
    motivo = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Motivo do Acesso',
        help_text='Ex: Consulta de Venda, Emissao de Nota Fiscal'
    )
    
    endereco_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='Endereco IP'
    )
    
    user_agent = models.TextField(
        blank=True,
        verbose_name='User-Agent do Navegador'
    )
    
    data_hora = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data e Hora do Acesso'
    )
    
    class Meta:
        verbose_name = 'Log de Acesso a Dados Sensiveis'
        verbose_name_plural = 'Logs de Acesso a Dados Sensiveis'
        ordering = ['-data_hora']
        indexes = [
            models.Index(fields=['usuario', '-data_hora']),
            models.Index(fields=['cliente_id', '-data_hora']),
            models.Index(fields=['tipo_dado', '-data_hora']),
        ]
    
    def __str__(self):
        return f"{self.usuario} acessou {self.tipo_dado} de {self.cliente_nome} em {self.data_hora.strftime('%d/%m/%Y %H:%M:%S')}"


class SolicitacaoLGPD(models.Model):
    """
    Modelo para registrar solicitacoes de direitos LGPD.
    
    Attributes:
        cliente_id: ID do cliente
        cliente_nome: Nome do cliente
        tipo_solicitacao: ACESSO, CORRECAO, DELECAO, PORTABILIDADE, OPOSICAO
        descricao: Descricao da solicitacao
        status: PENDENTE, EM_PROCESSAMENTO, CONCLUIDA, RECUSADA
        data_solicitacao: Data da solicitacao
        data_conclusao: Data da conclusao
        usuario_responsavel: Usuario que processou a solicitacao
        resposta: Resposta ou motivo da recusa
    """
    
    TIPO_SOLICITACAO_CHOICES = [
        ('ACESSO', 'Acesso aos Dados'),
        ('CORRECAO', 'Correcao de Dados'),
        ('DELECAO', 'Delecao de Dados'),
        ('PORTABILIDADE', 'Portabilidade de Dados'),
        ('OPOSICAO', 'Oposicao ao Processamento'),
    ]
    
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('EM_PROCESSAMENTO', 'Em Processamento'),
        ('CONCLUIDA', 'Concluida'),
        ('RECUSADA', 'Recusada'),
    ]
    
    cliente_id = models.PositiveIntegerField(
        verbose_name='ID do Cliente'
    )
    
    cliente_nome = models.CharField(
        max_length=255,
        verbose_name='Nome do Cliente'
    )
    
    tipo_solicitacao = models.CharField(
        max_length=20,
        choices=TIPO_SOLICITACAO_CHOICES,
        verbose_name='Tipo de Solicitacao'
    )
    
    descricao = models.TextField(
        verbose_name='Descricao da Solicitacao'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDENTE',
        verbose_name='Status'
    )
    
    data_solicitacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data da Solicitacao'
    )
    
    data_conclusao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data da Conclusao'
    )
    
    usuario_responsavel = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='solicitacoes_lgpd_processadas',
        verbose_name='Usuario Responsavel'
    )
    
    resposta = models.TextField(
        blank=True,
        verbose_name='Resposta ou Motivo da Recusa'
    )
    
    class Meta:
        verbose_name = 'Solicitacao LGPD'
        verbose_name_plural = 'Solicitacoes LGPD'
        ordering = ['-data_solicitacao']
        indexes = [
            models.Index(fields=['cliente_id', '-data_solicitacao']),
            models.Index(fields=['status', '-data_solicitacao']),
        ]
    
    def __str__(self):
        return f"{self.tipo_solicitacao} - {self.cliente_nome} - {self.status}"
    
    def marcar_concluida(self, usuario, resposta=''):
        """Marca a solicitacao como concluida."""
        self.status = 'CONCLUIDA'
        self.data_conclusao = timezone.now()
        self.usuario_responsavel = usuario
        self.resposta = resposta
        self.save()
    
    def marcar_recusada(self, usuario, motivo=''):
        """Marca a solicitacao como recusada."""
        self.status = 'RECUSADA'
        self.data_conclusao = timezone.now()
        self.usuario_responsavel = usuario
        self.resposta = motivo
        self.save()
