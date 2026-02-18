"""
Modelos do módulo de Clientes.

Este arquivo define os modelos de dados relacionados aos clientes do sistema.

Autor: Denis Barbosa (Todos os direitos reservados)
Data: 2026-02-17
"""

from django.db import models
from django.contrib.auth.models import User
from base.models import TenantModel
from django.core.validators import RegexValidator

class Cliente(TenantModel):
    """
    Modelo para armazenar informações de clientes.
    
    Agora o Cliente "percebe" a empresa herdando de TenantModel.
    """
    
    ESTADO_CHOICES = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ]
    
    nome = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(db_index=True)
    telefone = models.CharField(max_length=20, blank=True)
    cpf_cnpj = models.CharField(max_length=20, db_index=True)
    endereco = models.CharField(max_length=255, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES, blank=True)
    cep = models.CharField(max_length=10, blank=True)
    ativo = models.BooleanField(default=True, db_index=True)
    
    # LGPD - Conformidade com Lei Geral de Proteção de Dados
    consentimento_marketing = models.BooleanField(
        default=False,
        verbose_name="Consentimento para Marketing",
        help_text="Cliente autorizou recebimento de comunicações comerciais"
    )
    consentimento_dados = models.BooleanField(
        default=False,
        verbose_name="Consentimento de Dados",
        help_text="Cliente autorizou armazenamento e processamento de dados pessoais"
    )
    data_consentimento = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data do Consentimento",
        help_text="Data em que o cliente deu consentimento"
    )
    anonimizado = models.BooleanField(
        default=False,
        verbose_name="Dados Anonimizados",
        help_text="Indica se os dados pessoais foram removidos conforme LGPD"
    )
    data_anonimizacao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data da Anonimização"
    )
    
    # Auditoria
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_modificacao = models.DateTimeField(auto_now=True)
    usuario_criacao = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='clientes_criados'
    )
    usuario_modificacao = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='clientes_modificados'
    )
    
    class Meta:
        db_table = 'clientes_cliente'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']
        unique_together = [['company', 'cpf_cnpj'], ['company', 'email']]
        indexes = [
            models.Index(fields=['company', 'nome', 'ativo']),
            models.Index(fields=['company', 'email']),
            models.Index(fields=['company', 'cpf_cnpj']),
        ]
    
    def __str__(self):
        return f"{self.nome} ({self.company.name})" if self.company else self.nome
    
    def get_endereco_completo(self):
        """Retorna o endereço completo do cliente."""
        partes = [self.endereco, self.cidade, self.estado, self.cep]
        return ', '.join([p for p in partes if p])
    
    def anonimizar_dados(self, usuario):
        """Anonimiza dados pessoais conforme LGPD."""
        from datetime import datetime
        self.nome = f"Cliente Anonimizado #{self.id}"
        self.email = f"anonimizado_{self.id}@anonimizado.local"
        self.telefone = ""
        self.endereco = ""
        self.cidade = ""
        self.estado = ""
        self.cep = ""
        self.anonimizado = True
        self.data_anonimizacao = datetime.now()
        self.usuario_modificacao = usuario
        self.save()
        self.contatos.all().delete()


class ContatoCliente(models.Model):
    """
    Modelo para armazenar contatos adicionais de clientes.
    
    Permite múltiplos contatos por cliente (telefone, email, etc).
    """
    
    TIPO_CONTATO_CHOICES = [
        ('TELEFONE', 'Telefone'),
        ('EMAIL', 'Email'),
        ('CELULAR', 'Celular'),
        ('WHATSAPP', 'WhatsApp'),
    ]
    
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='contatos'
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CONTATO_CHOICES)
    valor = models.CharField(max_length=100)
    principal = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'clientes_contato'
        verbose_name = 'Contato do Cliente'
        verbose_name_plural = 'Contatos dos Clientes'
    
    def __str__(self):
        return f"{self.cliente.nome} - {self.tipo}: {self.valor}"
