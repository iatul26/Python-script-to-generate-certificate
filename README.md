# 🎓 Certificate Generator (Python)
A simple Python script to automatically generate **customized certificates in PDF format** using participant data from a CSV file.
This project overlays participant details like name, institute, topic, date, and serial number onto a certificate template image.

---
## 🚀 Features
* Generate certificates in **bulk from CSV**
* Automatically formats dates (e.g., `27th Jan` → `27 January 2024`)
* Centers text dynamically for clean alignment
* Exports certificates as **PDF files**
* Customizable font, positions, and layout
---
## 📂 Project Structure
```
.
├── template.png          # Certificate background template
├── font.ttf             # Font used for text
├── participants.csv     # Input data file
├── generated_certif/    # Output folder (auto-created)
├── generate.py              # Main script
```
---
## 🧾 CSV Format
Your `participants.csv` should contain the following columns:
```csv
participants,university,topic,date
participant1,ABC University,topic1,DDth MM YYYY
participant2,XYZ Institute,Data Science,DDth MM YYYY
```
---
## ⚙️ Configuration
You can customize positions, font sizes, and styling in the script:
```python
# Example
NAME_X = 874
NAME_Y = 645
FONT_SIZE = 42
TEXT_COLOR = (0, 0, 0)
```
Adjust these values based on your certificate template.
---
## 🛠️ Installation
### 1. Clone the repository
```bash
git clone https://github.com/iatul26/Python-script-to-generate-certificate.git
cd Python-script-to-generate-certificate
```
### 2. Install dependencies
```bash
pip install pandas pillow reportlab
```
---
## ▶️ Usage
1. Place your:
   * `template.png`
   * `font.ttf`
   * `participants.csv`
2. Run the script:
```bash
python generate.py
```
3. Generated certificates will be saved in:
```
generated_certif/
```
---
## 🧠 How It Works
* Loads participant data using **pandas**
* Cleans and formats date values
* Uses **Pillow (PIL)** to draw text on the template
* Centers text dynamically using width calculation
* Converts the final image into a **PDF using reportlab**
---
## ✨ Example Output
Each participant gets a certificate like:
```
participant1.pdf
participant2.pdf
```
---
## 🔧 Customization Ideas
* Add QR codes for verification
* Include signatures dynamically
* Export as PNG/JPG instead of PDF
* Add email automation to send certificates
---
## ⚠️ Notes
* Ensure the font file (`.ttf`) supports all characters
* CSV column names must match exactly:
  * `participants`
  * `university`
  * `topic`
  * `date`
---
## 📜 License
This project is open-source and available under the MIT License.
---
## 🙌 Contributing
Feel free to fork the repo and submit pull requests for improvements!
---
