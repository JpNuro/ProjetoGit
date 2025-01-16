from django.db import models

# Create your models here.

class Fruta(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField()
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Fruta'
        verbose_name_plural = 'Frutas'
