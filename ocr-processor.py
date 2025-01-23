import cv2
import pytesseract
from pyzbar.pyzbar import decode
import google.generativeai as genai
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

image_path = "yourimagepath"
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

custom_config = r"--psm 6"
text = pytesseract.image_to_string(gray, config=custom_config)

qr_codes = decode(image)
qr_data = [qr.data.decode("utf-8") for qr in qr_codes]

img = Image.open(image_path)

genai.configure(api_key="AIzaSyDKjjl8YuWmW07ZIAOLIEqrsJofP9cww5w")

if qr_data:
    input_text = f"""
    Extracted Text:
    {text}

    QR Codes Detected:
    {', '.join(qr_data) if qr_data else 'None'}
    """
else:
    input_text = f"""Extracted Text:
    {text}
    """

model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content(
    [
        f"Beautify the following text. Organize it with bullet points and headers where appropriate using only given text, do not add new text and do not bold or italic.:\n{input_text}",
        img,
    ],
    stream=True,
)

response.resolve()
beautified_text = response.text
print(beautified_text)
