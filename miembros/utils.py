import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from cloudinary.uploader import upload
import os


def generar_barcode_cloudinary(numero_carnet):
    """Genera código de barras y lo sube a Cloudinary"""
    try:
        ean_class = barcode.get_barcode_class('code128')
        if not ean_class:
            return None

        rv_buffer = BytesIO()
        ean_class(numero_carnet, writer=ImageWriter()).write(rv_buffer)
        rv_buffer.seek(0)

        if os.environ.get('CLOUDINARY_URL'):
            result = upload(rv_buffer, folder='carnets', resource_type='image')
            return result['secure_url']
        else:
            return None
    except Exception as e:
        print(f"Warning: Error generando barcode: {e}")
        return None
