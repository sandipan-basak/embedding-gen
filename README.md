# PDF Processing Pipeline

This repository hosts a pipeline specifically designed for chunking PDF documents into text segments and subsequently creating FAISS indices for these segments. It's particularly useful for applications that require efficient text search and retrieval from large collections of PDF documents.

## Overview

The pipeline facilitates two primary operations:
1. **Chunking PDF Dataset**: This step involves breaking down PDF documents into smaller, more manageable text chunks.
2. **Indexing Dataset**: This step involves creating FAISS indices from the text chunks, enabling efficient similarity searches across the dataset.

## Getting Started

### Prerequisites

- Docker installed on your machine
- A collection of PDF documents you wish to process

### Configuration

Pipeline operations are controlled through the `PIPELINE_STEP` variable within a `.env` file. Here's how to set it up:

1. Create a `.env` file in the root directory of the project.
2. Add the following line to configure the pipeline for either chunking or indexing:
   - For chunking PDFs into text segments:
     ```
     PIPELINE_STEP=1
     ```
   - For indexing the chunked text segments:
     ```
     PIPELINE_STEP=2
     ```

### Running with Docker

The provided Dockerfile allows for easy containerization and execution of the pipeline, abstracting away the need for manual Python environment setup and dependency management.

#### Building the Docker Image

From the project's root directory, execute the following command to build the Docker image:

```bash
docker build -t pdf_processing_pipeline .

docker run -p 80:80 --env-file ./.env pdf_processing_pipeline
