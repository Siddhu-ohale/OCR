
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

def extract_raw_text(image_path):
    image = Image.open(image_path).convert("L")
    image = image.filter(ImageFilter.SHARPEN)
    image = ImageEnhance.Contrast(image).enhance(2.0)
    image = image.resize((image.width * 2, image.height * 2))
    return pytesseract.image_to_string(image, config='--oem 3 --psm 6')
