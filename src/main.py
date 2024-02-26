from process_data import read_and_preprocess_pdfs

def main():
    print("Starting indexing pipeline...")
    startpipeline()

def startpipeline():
    print("Starting PDF extraction pipeline...")

    # reading from pdf and extracting texts
    read_and_preprocess_pdfs()

if __name__ == "__main__":
    main()