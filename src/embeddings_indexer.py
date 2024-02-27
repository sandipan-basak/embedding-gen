import os
import faiss
import numpy as np
# from openai import OpenAI
from fastembed import TextEmbedding

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def store_chunk_data():
    base_dir="/usr/src/app/data"
    chunks_dir = os.path.join(base_dir, "chunks")
    indices_dir = os.path.join(base_dir, "indices")
    os.makedirs(indices_dir, exist_ok=True)
    all_embeddings = []

    for root, dirs, files in os.walk(chunks_dir):
        for file in files:
            chunk_data_path = os.path.join(root, file)
            chunk_data = read_chunk_data(chunk_data_path)

            max_length = 1024
            chunks = split_text(chunk_data, max_length)

            if chunks:
                cleaned_chunks = [chunk.replace('\n', ' ') for chunk in chunks]
                for chunk in cleaned_chunks:
                    embeddings = get_embeddings(chunk)
                    all_embeddings.extend(embeddings)
    
    if all_embeddings:
        all_embeddings_array = np.array(all_embeddings)
        faiss_index = create_faiss_index(all_embeddings_array)

        index_file = os.path.join(indices_dir, "combined_index")
        faiss.write_index(faiss_index, index_file + ".index")
        print(f"Combined FAISS index stored as {index_file}")


def split_text(text, max_length):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]


def read_chunk_data(filepath):
    with open(filepath, 'r') as file:
        chunk_data = file.read()
    return chunk_data


def get_embeddings(text):
    embedding_model = TextEmbedding(model_name="BAAI/bge-base-en")
    embeddings = list(embedding_model.embed(text))
    return embeddings


def create_faiss_index(embeddings):
    # Check if embeddings is a 3D array and attempt to convert it to 2D
    if len(embeddings.shape) == 3:
        print(f"Original embeddings shape (3D): {embeddings.shape}")
        # Assuming the third dimension is unnecessary, you can squeeze it
        # Check if the third dimension is 1, which makes it safe to squeeze
        if embeddings.shape[2] == 1:
            embeddings = np.squeeze(embeddings, axis=2)
        else:
            # If the third dimension is not 1, you need to decide how to handle this case
            # For example, you might need to average the vectors, select one, or flatten them
            embeddings = embeddings.reshape(-1, embeddings.shape[-1])
        print(f"Reshaped embeddings shape (2D): {embeddings.shape}")
    elif len(embeddings.shape) != 2:
        raise ValueError("After processing, embeddings must be a 2D numpy array.")
    
    dimension = embeddings.shape[1]  # Get the dimension of embeddings
    index = faiss.IndexFlatL2(dimension)  # Create a FAISS index of the appropriate dimension
    index.add(embeddings)  # Add embeddings to the index
    return index
