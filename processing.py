import os

import tqdm

from chunking import split_text_into_chunks
from src.database.qdrant.qdrant_search import QdrantSearchBGE
from parsers.docx_parser import parse_doc_file
from parsers.image_parser import TextExtractorFromImage
from parsers.pdf_parser import parse_pdf_file
from parsers.txt_parser import parse_txt_file


def process_folder(
    folder_path: str,
    searcher: QdrantSearchBGE(collection_name="diseases_collection"),
    chunk_size: int = 800,
    overlap: int = 50,
    text_extractor=TextExtractorFromImage(device="cpu")):
    """
    Duyệt toàn bộ file trong folder, trích xuất văn bản, chunk và insert vào Qdrant.

    Args:
        folder_path (str): Đường dẫn đến thư mục chứa file.
        searcher (QdrantSearch_bge): Đối tượng Qdrant để insert chunk.
        chunk_size (int): Độ dài tối đa mỗi chunk.
        overlap (int): Ký tự chồng lặp giữa các chunk.
    """
    supported_images = [".png", ".jpg", ".jpeg"]
    supported_docs = [".doc", ".docx"]
    supported_pdfs = [".pdf"]
    supported_txts = [".txt"]

    for filename in tqdm.tqdm(os.listdir(folder_path)):
        print(f"\nProcessing file: {filename}")
        file_path = os.path.join(folder_path, filename)
        ext = os.path.splitext(filename)[1].lower()

        extracted_texts = []

        if ext in supported_pdfs:
            extracted_texts = parse_pdf_file(file_path)
        elif ext in supported_docs:
            extracted_texts = parse_doc_file(file_path)
        elif ext in supported_images:
            extracted_texts = text_extractor.parse_img_file(file_path)
        elif ext in supported_txts:
            extracted_texts = parse_txt_file(file_path)
        else:
            print(f"Skipped unsupported file: {filename}")
            continue

        # Chunk và insert into Qdrant
        for text in extracted_texts:
            chunks = split_text_into_chunks(text, chunk_size=chunk_size, chunk_overlap=overlap)
            searcher.insert(chunks)

    print(f"Processing and indexing successful")

if __name__ == "__main__":
    # Define folder paths
    # pdf_folder = "data/diseases"
    txt_folder = "data/healthcare_data"

    # Initialize Qdrant searcher
    searcher = QdrantSearchBGE(collection_name="diseases_collection", model_name="BAAI/bge-m3", use_fp16=False)

    # Process PDF files
    # if os.path.exists(pdf_folder):
    #     process_folder(pdf_folder, searcher)
    # else:
    #     print(f"PDF folder not found: {pdf_folder}")

    # Process TXT files
    if os.path.exists(txt_folder):
        process_folder(txt_folder, searcher)
    else:
        print(f"TXT folder not found: {txt_folder}")

    print("Processing and indexing completed successfully")