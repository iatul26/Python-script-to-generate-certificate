import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# Configuration
TEMPLATE = "template.png"
FONT_PATH = "font.ttf"
FONT_SIZE = 45
TEXT_COLOR = (255, 255, 255)
NAME_X = 500
NAME_Y = 500
OUTPUT_DIR = "generated_certif"
CSV_FILE = "participants.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load resources 
data = pd.read_csv(CSV_FILE)
base_img = Image.open(TEMPLATE).convert("RGB")
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

img_width, img_height = base_img.size

# Process
for name in data["name"].dropna():
    safe_name = name.strip().replace("/", "_")

    img = base_img.copy()
    draw = ImageDraw.Draw(img)

    text_width = draw.textlength(name, font=font)
    x = NAME_X - text_width // 2

    draw.text((x, NAME_Y), name, fill=TEXT_COLOR, font=font)

    pdf_path = os.path.join(OUTPUT_DIR, f"{safe_name}.pdf")

    c = canvas.Canvas(pdf_path, pagesize=(img_width, img_height))
    c.drawImage(ImageReader(img), 0, 0, width=img_width, height=img_height)
    c.save()

print("Certificates generated successfully.")