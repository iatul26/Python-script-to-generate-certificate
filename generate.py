import os
import re
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# ---------------- CONFIG ----------------
TEMPLATE = "template.png"
FONT_PATH = "font.ttf"
TEXT_COLOR = (0, 0, 0)

# Name
FONT_SIZE = 42
NAME_X = 874
NAME_Y = 645

# Institute
UNI_X = 850
UNI_Y = 700
UNI_FONT_SIZE = 32

# Topic
TOPIC_X = 520
TOPIC_Y = 1030
TOPIC_FONT_SIZE = 32

# Date
DATE_X = 1570
DATE_Y = 1030
DATE_FONT_SIZE = 28

# Serial Number
SRNO_X = 500
SRNO_Y = 1345
SRNO_FONT_SIZE = 27

OUTPUT_DIR = "generated_certif"
CSV_FILE = "participants.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------- DATE CLEANER ----------------
def clean_date(date):
    if pd.isna(date):
        return ""

    date = str(date)

    # remove st, nd, rd, th (27th → 27)
    date = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date)

    try:
        return pd.to_datetime(date).strftime("%d %B %Y")
    except:
        return date

# ---------------- LOAD DATA ----------------
data = pd.read_csv(CSV_FILE, skipinitialspace=True)

# ---------------- TEMPLATE ----------------
base_img = Image.open(TEMPLATE).convert("RGB")
img_width, img_height = base_img.size

# ---------------- FONTS ----------------
name_font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
uni_font = ImageFont.truetype(FONT_PATH, UNI_FONT_SIZE)
topic_font = ImageFont.truetype(FONT_PATH, TOPIC_FONT_SIZE)
date_font = ImageFont.truetype(FONT_PATH, DATE_FONT_SIZE)
sr_font = ImageFont.truetype(FONT_PATH, SRNO_FONT_SIZE)

# ---------------- PROCESS ----------------
for i, (_, row) in enumerate(data.iterrows(), start=1):

    # Extract fields using column names
    name = str(row["participants"]).strip()
    institute = str(row["university"]).strip() if pd.notna(row["university"]) else ""
    topic = str(row["topic"]).strip() if pd.notna(row["topic"]) else ""
    date = clean_date(row["date"])

    # Safe filename
    safe_name = re.sub(r'[^\w\s-]', '', name).strip()

    # Create image
    img = base_img.copy()
    draw = ImageDraw.Draw(img)

    # ---- Draw Name ----
    text_width = draw.textlength(name, font=name_font)
    x = NAME_X - text_width // 2
    draw.text((x, NAME_Y), name, fill=TEXT_COLOR, font=name_font)

    # ---- Draw Institute ----
    uni_width = draw.textlength(institute, font=uni_font)
    uni_x = UNI_X - uni_width // 2
    draw.text((uni_x, UNI_Y), institute, fill=TEXT_COLOR, font=uni_font)

    # ---- Draw Topic ----
    topic_width = draw.textlength(topic, font=topic_font)
    topic_x = TOPIC_X - topic_width // 2
    draw.text((topic_x, TOPIC_Y), topic, fill=TEXT_COLOR, font=topic_font)

    # ---- Draw Date ----
    date_width = draw.textlength(date, font=date_font)
    date_x = DATE_X - date_width // 2
    draw.text((date_x, DATE_Y), date, fill=TEXT_COLOR, font=date_font)

    # ---- Draw Serial Number ----
    sr_text = f"{i:03d}"
    sr_width = draw.textlength(sr_text, font=sr_font)
    sr_x = SRNO_X - sr_width // 2
    draw.text((sr_x, SRNO_Y), sr_text, fill=TEXT_COLOR, font=sr_font)

    # ---- Save PDF ----
    pdf_path = os.path.join(OUTPUT_DIR, f"{safe_name}.pdf")

    c = canvas.Canvas(pdf_path, pagesize=(img_width, img_height))
    c.drawImage(ImageReader(img), 0, 0, width=img_width, height=img_height)
    c.save()

print("Certificates generated successfully.")
