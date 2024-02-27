import os
from process_data import read_and_preprocess_pdfs
from embeddings_indexer import store_chunk_data
from dotenv import load_dotenv

load_dotenv()

def main():
    start_pipeline()


def start_pipeline():
    if os.getenv("PIPELINE_STEP") == '1':
        # reading from pdf and extracting processed text chunks
        print("Starting chunking pipeline...")
        read_and_preprocess_pdfs()

    elif os.getenv("PIPELINE_STEP") == '2':
        # creating and storing FAISS indices
        print("Starting indexing pipeline...")
        store_chunk_data()


if __name__ == "__main__":
    main()