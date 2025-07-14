import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm import tqdm
from underthesea import sent_tokenize

from logger import logger


def split_text_into_chunks(text: str, chunk_size: int=400, chunk_overlap: int=80):
    """Split a long text into chunks using LangChain, preserving sentence boundaries.

    Args:
        text (str): Input text to split.
        chunk_size (int): Maximum number of words per chunk
        chunk_overlap (int): Number of words to overlap between chunks (default: 80).
    Returns:
        List[str]: List of text chunks.
    """
    try:
        # Chia văn bản thành câu bằng underthesea để giữ ngữ nghĩa
        sentences = sent_tokenize(text)
        text = " ".join(sentences)  # Ghép lại thành văn bản liên tục

        # Khởi tạo RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=lambda t: len(t.split()),  # Đếm số từ
            separators=["\n\n", "\n", ".", " "],  # Ưu tiên chia theo đoạn, câu
            keep_separator=True  # Giữ dấu phân cách trong chunk
        )

        # Chia văn bản thành chunks
        chunks = text_splitter.split_text(text)
        logger.info(f"Chia {len(text.split())} từ thành {len(chunks)} chunks")
        return chunks
    except Exception as e:
        logger.error(f"Lỗi khi chia chunk: {str(e)}")
        return []

def get_corpus(data_dir="data/healthcare_data/"):
    """Transform a corpus of documents into a corpus of passages using LangChain.
    Args:
        data_dir (str): Directory containing .txt files.
    Returns:
        List[dict]: A corpus of chunks with metadata (id, title, passage, len).
    """
    corpus = []
    meta_corpus = []
    filenames = sorted(os.listdir(data_dir))
    _id = 0

    for filename in tqdm(filenames):
        filepath = os.path.join(data_dir, filename)
        try:
            title = filename.replace(".txt", "")
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read().strip()
                # Chia văn bản thành chunks bằng LangChain
                chunks = split_text_into_chunks(text, chunk_size=400, chunk_overlap=80)
                # Thêm title vào mỗi chunk
                chunks = [f"Title: {title}\n\n{chunk}" for chunk in chunks]
                # Tạo metadata cho mỗi chunk
                meta_chunks = [{
                    "title": title,
                    "passage": chunk,
                    "id": _id + i,
                    "len": len(chunk.split())
                } for i, chunk in enumerate(chunks)]
                _id += len(chunks)
                corpus.extend(chunks)
                meta_corpus.extend(meta_chunks)
        except Exception as e:
            logger.error(f"Error when handle file {filename}: {str(e)}")
            continue

    logger.info(f"Create corpus with {len(meta_corpus)} chunks from {len(filenames)} documents")
    return meta_corpus