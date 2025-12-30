from PIL import Image
import pillow_heif

# Register HEIC opener with PIL
pillow_heif.register_heif_opener()

# Open and convert HEIC to JPG
heic_path = "images/IMG_20251209_090844.heic"
jpg_path = "images/gregory-st-kitts.jpg"

img = Image.open(heic_path)
img.convert("RGB").save(jpg_path, "JPEG", quality=95)

print(f"✅ Converted! Saved as: {jpg_path}")
print(f"Image size: {img.size[0]}x{img.size[1]} pixels")
