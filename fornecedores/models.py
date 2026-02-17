from django.db import models
from django.contrib.auth.models import User
from companies.models import Company

class Fornecedor(models.Model):
    """
    Modelo para armazenar informações de fornecedores.
    
    Atributos:
        nome: Nome do fornecedor
        email: Email do fornecedor
        telefone: Telefone do fornecedor
        cnpj: CNPJ do fornecedor
        endereco: Endereço do fornecedor
        cidade: Cidade do fornecedor
        estado: Estado do fornecedor
        cep: CEP do fornecedor
        ativo: Se o fornecedor está ativo
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
    
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='fornecedores_app',
        verbose_name="Empresa",
        null=True,
        blank=True
    )
    nome = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(db_index=True)
    telefone = models.CharField(max_length=20, blank=True)
    cnpj = models.CharField(max_length=20, db_index=True)
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
        related_name='fornecedores_app_criados'
    )
    usuario_modificacao = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='fornecedores_app_modificados'
    )
    
    class Meta:
        db_table = 'fornecedores_fornecedor'
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['nome']
        unique_together = [['company', 'cnpj'], ['company', 'email']]
        indexes = [
            models.Index(fields=['company', 'nome', 'ativo']),
            models.Index(fields=['company', 'email']),
            models.Index(fields=['company', 'cnpj']),
        ]
    
    def __str__(self):
        return f"{self.nome} ({self.cnpj})"
    
    def get_endereco_completo(self):
        """Retorna o endereço completo do fornecedor."""
        partes = [self.endereco, self.cidade, self.estado, self.cep]
        return ', '.join([p for p in partes if p])


class ContatoFornecedor(models.Model):
    """
    Modelo para armazenar contatos adicionais de fornecedores.
    
    Permite múltiplos contatos por fornecedor (telefone, email, etc).
    """
    
    TIPO_CONTATO_CHOICES = [
        ('TELEFONE', 'Telefone'),
        ('EMAIL', 'Email'),
        ('CELULAR', 'Celular'),
        ('WHATSAPP', 'WhatsApp'),
    ]
    
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.CASCADE,
        related_name='contatos'
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CONTATO_CHOICES)
    valor = models.CharField(max_length=100)
    principal = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'fornecedores_contato'
        verbose_name = 'Contato do Fornecedor'
        verbose_name_plural = 'Contatos dos Fornecedores'
    
    def __str__(self):
        return f"{self.fornecedor.nome} - {self.tipo}: {self.valor}"
