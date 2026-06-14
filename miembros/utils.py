import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from cloudinary.uploader import upload
import os


def generar_barcode_cloudinary(numero_carnet):
    """Genera código de barras y lo sube a Cloudinary"""
    ean = barcode.get_barcode_class('code128')
    rv_buffer = BytesIO()
    ean(numero_carnet, writer=ImageWriter()).write(rv_buffer)
    rv_buffer.seek(0)

    if os.environ.get('CLOUDINARY_URL'):
        result = upload(rv_buffer, folder='carnets', resource_type='image')
        return result['secure_url']
    else:
        return None
