import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageEnhance

class ImageProcessor:
    @staticmethod
    def apply_filter(image: Image.Image, filter_name: str) -> Image.Image:
        filter_map = {
            "sketch": ImageProcessor._sketch_filter,
            "emboss": lambda img: img.filter(ImageFilter.EMBOSS),
            "oil_paint": lambda img: img.filter(ImageFilter.ModeFilter(size=5)),
            "posterize": lambda img: ImageOps.posterize(img, bits=3),
            "vintage": ImageProcessor._vintage_filter
        }
        return filter_map.get(filter_name.lower(), lambda img: img)(image)

    @staticmethod
    def _sketch_filter(image: Image.Image) -> Image.Image:
        gray = image.convert("L")
        inv = ImageOps.invert(gray)
        blur = inv.filter(ImageFilter.GaussianBlur(radius=10))
        g = np.array(gray, float)
        b = np.array(blur, float)
        dodge = np.clip(g * 255 / (255 - b + 1e-6), 0, 255).astype('uint8')
        return Image.fromarray(dodge).convert("RGB")

    @staticmethod
    def _vintage_filter(image: Image.Image) -> Image.Image:
        e = ImageEnhance.Contrast(image).enhance(0.9)
        return ImageOps.colorize(e.convert("L"), black="#40210f", white="#f0e5d8")