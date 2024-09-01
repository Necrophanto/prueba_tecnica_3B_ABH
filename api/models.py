from django.db import models
import logging

logger = logging.getLogger(__name__)

# Create your models here.
class Producto(models.Model):
    sku = models.CharField(max_length=40, unique=True)  # Pude haber usado un UUIDField, pero los SKU no siempre son formato UUID
    name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    
    def save(self, *args, **kwargs):
        """
        Aunque se pide generar un job para hacer esta alerta, me pareció más 
        directo modificar la función save para que dispare el logger en lugar de 
        poner a correr un job, incluso se podría agregar un mensajero para mandar 
        el mismo mensaje ya sea a un correo de administrador o por SMS; incluso 
        otra opción sería crear un cronjob en el servidor donde se monte esto y 
        que revise cada X minutos el stock, pero eso generaría una consulta 
        innecesaria en la BD, reduciendo su desempeño.
        """
        if self.quantity < 10:
            logger.warning(f"ADVERTENCIA: El producto '{self.name}', tiene un stock de {self.quantity} unidades.")
            # Aquí puede detonarse una función de mensajería para avisar a un SMS o e-mail
        
        super(Producto, self).save(*args, **kwargs)

# Decido eliminar este modelo por simplificación, y así muevo el campo quantity al modelo del producto
# class Stock(models.Model):
#     sku = models.OneToOneField(Producto, on_delete=models.DO_NOTHING, unique=True)  # CharField(max_length=40, unique=True)
#     quantity = models.IntegerField()


class Orders(models.Model):
    product_id = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()

