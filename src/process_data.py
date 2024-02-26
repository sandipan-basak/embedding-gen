import os
import re
import fitz

def read_and_preprocess_pdfs():
    pdf_dir = "/usr/src/app/data/"
    for root, dirs, files in os.walk(pdf_dir):
        for file in files:
            full_path = os.path.join(root, file)
            if file.endswith(".PDF") or file.endswith(".pdf"):
                print(f"Processing {file}")
                final_chunk = extract_text_from_pdf(full_path)
                print(final_chunk)


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        raw_text = page.get_text()
        text += preprocess_text_chunk(raw_text)
    doc.close()
    return text


def preprocess_text_chunk(text):
    text = re.sub('<[^<]+?>', '', text)
    text = re.sub('[^0-9a-zA-Z]+', ' ', text)
    return text