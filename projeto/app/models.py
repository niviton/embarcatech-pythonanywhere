from django.db import models

# Create your models here.
class Reservatorio(models.Model):
    capacidade_total = models.FloatField()
    litros_restantes = models.FloatField()
    porcentagem_agua = models.FloatField()
    umidade = models.FloatField()
    distancia_agua = models.FloatField()
    vazao_agua = models.FloatField()
    irrigacoes_restantes = models.IntegerField()
    estado = models.CharField(max_length=50)

    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservatorio {self.id} - Estado: {self.estado}"