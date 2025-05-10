import cv2
import pytesseract
from pyzbar.pyzbar import decode
import google.generativeai as genai
from PIL import Image
import keras_ocr
import firebase_admin
from firebase_admin import credentials, firestore

# Configure API Key for Generative AI
GENAI_API_KEY = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=GENAI_API_KEY)

# Configure Tesseract Path
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

# Initialize Firebase
FIREBASE_CREDENTIALS_PATH = "D:/vat-demo-f206b-firebase-adminsdk-fbsvc-e8d3543a25.json"
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Process OCR functionality through an image file
def process_image_ocr(image_path):
    """Processes an image to extract text and QR codes using OCR."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    custom_config = r"--psm 6"
    text = pytesseract.image_to_string(gray, config=custom_config)

    qr_codes = decode(image)
    qr_data = [qr.data.decode("utf-8") for qr in qr_codes]

    img = Image.open(image_path)

    input_text = f"""
    Extracted Text:
    {text}

    QR Codes Detected:
    {', '.join(qr_data) if qr_data else 'None'}
    """

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(
        [f"Beautify the following text:\n{input_text}", img], stream=True
    )
    response.resolve()
    beautified_text = response.text

    print("Beautified Extracted Text:\n", beautified_text)


# Process OCR functionality through a live video capturing
def process_live_feed_ocr():
    """Processes live video feed and extracts text using OCR."""
    cap = cv2.VideoCapture(0)
    pipeline = keras_ocr.pipeline.Pipeline()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        prediction_groups = pipeline.recognize([frame_rgb])

        for predictions in prediction_groups[0]:
            box = predictions[1]
            cv2.polylines(frame, [box.astype(int)], True, (0, 255, 0), 2)
            text = predictions[0]
            position = tuple(box[0].astype(int))
            cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow('Live OCR', frame)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            extracted_text = " ".join([predictions[0] for predictions in prediction_groups[0]])
            input_text = f"Extracted Text:\n{extracted_text}"

            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(
                [f"Beautify the following text:\n{input_text}"],
                stream=True
            )
            response.resolve()
            beautified_text = response.text

            # Store beautified text in Firebase
            doc_ref = db.collection("ocr_texts").document()
            doc_ref.set({"text": beautified_text})

            print("Beautified Text Saved to Firebase!")
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    """Main function to choose between image or live OCR processing."""
    print("Select Mode:")
    print("1. Image OCR")
    print("2. Live Video Feed OCR")
    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        image_path = input("Enter image path: ").strip()
        process_image_ocr(image_path)
    elif choice == "2":
        process_live_feed_ocr()
    else:
        print("Invalid choice! Please enter 1 or 2.")


if __name__ == "__main__":
    main()
