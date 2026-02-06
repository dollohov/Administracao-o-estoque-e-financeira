from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Cliente(models.Model):
    """
    Modelo para armazenar informações de clientes.
    
    Atributos:
        nome: Nome do cliente
        email: Email do cliente
        telefone: Telefone do cliente
        cpf_cnpj: CPF ou CNPJ do cliente
        endereco: Endereço do cliente
        cidade: Cidade do cliente
        estado: Estado do cliente
        cep: CEP do cliente
        ativo: Se o cliente está ativo
        data_criacao: Data de criação do registro
        data_modificacao: Data da última modificação
        usuario_criacao: Usuário que criou o registro
        usuario_modificacao: Usuário que modificou o registro
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
    email = models.EmailField(unique=True, db_index=True)
    telefone = models.CharField(max_length=20, blank=True)
    cpf_cnpj = models.CharField(max_length=20, unique=True, db_index=True)
    endereco = models.CharField(max_length=255, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES, blank=True)
    cep = models.CharField(max_length=10, blank=True)
    ativo = models.BooleanField(default=True, db_index=True)
    
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
        indexes = [
            models.Index(fields=['nome', 'ativo']),
            models.Index(fields=['email']),
            models.Index(fields=['cpf_cnpj']),
        ]
    
    def __str__(self):
        return f"{self.nome} ({self.cpf_cnpj})"
    
    def get_endereco_completo(self):
        """Retorna o endereço completo do cliente."""
        partes = [self.endereco, self.cidade, self.estado, self.cep]
        return ', '.join([p for p in partes if p])


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
