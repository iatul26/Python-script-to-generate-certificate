import os
import re
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# Configuration
TEMPLATE = "template.png"
FONT_PATH = "font.ttf"
FONT_SIZE = 42
TEXT_COLOR = (0, 0, 0)

NAME_X = 915
NAME_Y = 660

UNI_X = 955
UNI_Y = 725
UNI_FONT_SIZE = 32

SRNO_X = 465
SRNO_Y = 1305
SRNO_FONT_SIZE = 27

OUTPUT_DIR = "generated_certif"
CSV_FILE = "participants.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load CSV
data = pd.read_csv(CSV_FILE)

# Load template
base_img = Image.open(TEMPLATE).convert("RGB")
img_width, img_height = base_img.size

# Fonts
name_font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
uni_font = ImageFont.truetype(FONT_PATH, UNI_FONT_SIZE)
sr_font = ImageFont.truetype(FONT_PATH, SRNO_FONT_SIZE)

# Process certificates
for i, (_, row) in enumerate(data.iterrows(), start=1):

    name = str(row.iloc[0]).strip()

    college = row.iloc[1] if len(row) > 1 else None
    university = row.iloc[2] if len(row) > 2 else None

    # choose whichever exists
    if pd.notna(college) and str(college).strip() != "":
        institute = str(college).strip()
    elif pd.notna(university) and str(university).strip() != "":
        institute = str(university).strip()
    else:
        institute = ""

    # safe filename
    safe_name = re.sub(r'[^\w\s-]', '', name).strip()

    img = base_img.copy()
    draw = ImageDraw.Draw(img)

    # Draw Name
    text_width = draw.textlength(name, font=name_font)
    x = NAME_X - text_width // 2
    draw.text((x, NAME_Y), name, fill=TEXT_COLOR, font=name_font)

    # Draw Institute
    uni_text_width = draw.textlength(institute, font=uni_font)
    uni_x = UNI_X - uni_text_width // 2
    draw.text((uni_x, UNI_Y), institute, fill=TEXT_COLOR, font=uni_font)

    # Draw Serial Number
    sr_text = f"{i:03d}"
    sr_width = draw.textlength(sr_text, font=sr_font)
    sr_x = SRNO_X - sr_width // 2
    draw.text((sr_x, SRNO_Y), sr_text, fill=TEXT_COLOR, font=sr_font)

    # Save PDF
    pdf_path = os.path.join(OUTPUT_DIR, f"{safe_name}.pdf")

    c = canvas.Canvas(pdf_path, pagesize=(img_width, img_height))
    c.drawImage(ImageReader(img), 0, 0, width=img_width, height=img_height)
    c.save()

print("Certificates generated successfully.")
