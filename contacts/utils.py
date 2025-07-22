from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
import random
import string

def generate_initials_image(initials, size=(150, 150), bg_color=None):
    # Choix aléatoire de couleur si non donnée
    if bg_color is None:
        bg_color = random.choice(['#3498db', '#e67e22', '#1abc9c', '#9b59b6'])

    # Crée une image carrée
    image = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(image)

    # Utilise une police basique de PIL
    font_size = int(size[0] * 0.4)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # Centrer les initiales
    text_width, text_height = draw.textsize(initials, font=font)
    position = ((size[0] - text_width) / 2, (size[1] - text_height) / 2)
    draw.text(position, initials.upper(), fill='white', font=font)

    # Sauvegarde l’image dans un fichier mémoire
    temp_file = BytesIO()
    image.save(temp_file, format='PNG')
    temp_file.seek(0)

    return ContentFile(temp_file.read(), name='initials_{}.png'.format(''.join(random.choices(string.ascii_lowercase, k=5))))
