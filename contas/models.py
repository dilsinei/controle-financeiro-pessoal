# contas/models.py


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Transacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    # data = models.DateField(auto_now_add=True)
    data = models.DateField(null=True, blank=True)

    tipo = models.CharField(
        max_length=20,
        choices=[
            ("Receita", "Receita"),
            (
                "Despesa",
                "Despesa",
            ),
        ],
    )

    def __str__(self):
        return f"{self.tipo}: {self.descricao} - R${self.valor}"

    def save(self, *args, **Kwargs):
        if not self.data:
            self.data = timezone.now().date()
        super().save(*args, **Kwargs)
