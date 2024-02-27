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
                extract_text_from_pdf(file, full_path, pdf_dir)


def extract_text_from_pdf(file, pdf_path, pdf_dir):
    doc = fitz.open(pdf_path)

    for page_number, page in enumerate(doc):
        raw_text = page.get_text()
        processed_text = preprocess_text_chunk(raw_text)
        store_chunk_file(processed_text, file, pdf_dir, page_number + 1)

    doc.close()


def preprocess_text_chunk(text):
    text = re.sub('<[^<]+?>', '', text)

    # removing this filtering to not miss out on important factual analysis of the page chunking
    # text = re.sub('[^0-9a-zA-Z]+', ' ', text)
    return text


def store_chunk_file(chunk, file, pdf_dir, chunk_number):
    chunk_dir = os.path.join(pdf_dir, 'chunks', file[:-4])
    os.makedirs(chunk_dir, exist_ok=True)
    output_file_path = os.path.join(chunk_dir, f'chunk_data_{chunk_number}.txt')

    with open(output_file_path, 'w') as output_file:
        output_file.write(chunk)
    print(f"Final chunk data written to {output_file_path}")