from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Miembro, Carnet
from .utils import generar_barcode_cloudinary


@receiver(post_save, sender=Miembro)
def crear_carnet_automatico(sender, instance, created, **kwargs):
    if created:
        numero_carnet = f"CS-{instance.id:05d}"

        barcode_url = generar_barcode_cloudinary(numero_carnet)

        if barcode_url:
            Carnet.objects.create(
                miembro=instance,
                numero_carnet=numero_carnet,
                codigo_barras_imagen=barcode_url
            )
        else:
            Carnet.objects.create(
                miembro=instance,
                numero_carnet=numero_carnet,
                codigo_barras_imagen='placeholder.png'
            )
