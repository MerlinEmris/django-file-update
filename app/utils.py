from PIL import Image
from io import BytesIO

from django.core.files import File


def compress(image):
    """
        Takes image and converts it to JPEG format with compession
    """
    print('image compress -> ', image.path)
    im = Image.open(image)
    im_io = BytesIO() 
    im.save(im_io, 'JPEG', quality=85) 
    new_image = File(im_io, name=image.name)
    return new_image