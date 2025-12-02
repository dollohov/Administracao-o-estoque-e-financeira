from django.db import models

class Receita(models.Model):
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()

    def __str__(self):
        return f"Receita: {self.descricao} ({self.valor})"

class Despesa(models.Model):
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()

    def __str__(self):
        return f"Despesa: {self.descricao} ({self.valor})"

    class Meta:
        verbose_name_plural = "Despesas"
