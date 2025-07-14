import uuid

from FlagEmbedding import BGEM3FlagModel
from qdrant_client import models
from qdrant_client.models import PointStruct

from logger import logger
from src.database.qdrant.config import get_qdrant_client


class QdrantSearchBGE:
    def __init__(self, collection_name: str, embedding_model_name: str = "BAAI/bge-m3", use_fp16:
    bool = False):
        """
            Init Qdrant client and embedding model
            Args:
                collection_name (str): Collection Qdrant
                embedding_model_name (str): default - BAAI/bge-m3
        """
        try:
            self.client = get_qdrant_client()
            self.collection_name = collection_name
            self.model_embedding = BGEM3FlagModel(embedding_model_name, use_fp16=use_fp16)

            # Create collection if not exist
            if not self.client.collection_exists(self.collection_name):
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE)
                )
        except Exception as e:
            logger.error(f"Error init QdrantSearchBGE: {str(e)}")
            raise

    def encode(self, text: str) -> list:
        """
        Encode text to vector embedding
        Returns:
            list: Vector embedding
        """
        try:
            embedding = self.model_embedding.encode(text, return_dense=True, return_sparse=False, return_colbert_vecs=False)
            return embedding['dense_vecs'].tolist()
        except Exception as e:
            logger.error(f"Error encode: {str(e)}")
            raise

    def insert(self, texts: list):
        """
        Insert vector to Qdrant
        Args:
            texts (list): List of texts to insert into Qdrant collection.
        """
        try:
            points = []
            for text in texts:
                dense_vec = self.encode(text)
                points.append(
                    PointStruct(
                        id=uuid.uuid4().hex,
                        vector=dense_vec,
                        payload={"text": text}
                    )
                )
            self.client.upsert(collection_name=self.collection_name, points=points)
            logger.info(f"Đã chèn {len(points)} điểm vào collection '{self.collection_name}'")
        except Exception as e:
            logger.error(f"Lỗi khi chèn dữ liệu vào Qdrant: {str(e)}")
            raise

    def search(self, query_text: str, limit: int = 10) -> list:
        """
        Tìm kiếm các đoạn văn bản tương tự nhất trong Qdrant dựa trên câu hỏi.
        Args:
            query_text (str): Câu truy vấn từ người dùng.
            limit (int): Số kết quả trả về.

        Returns:
            list: Danh sách kết quả gần đúng nhất kèm payload.
        """
        # Encode câu truy vấn query_text thành vector
        query_vector = self.encode(query_text)
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            with_payload=True
        )
        logger.info(f"Tìm kiếm thành công với query: {query_text}, trả về {len(results)} kết quả")
        return results


    def count_records(self) -> int:
        """
        Returns:
            int: Number of current records.
        """
        count = self.client.count(collection_name=self.collection_name, exact=True).count
        logger.info(f"Count records in collection '{self.collection_name}': {count}")
        return count
