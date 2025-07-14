from typing import List

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from logger import logger
from src.database.qdrant.qdrant_search import QdrantSearchBGE
from src.reranker import Reranker
from src.rewrite_query import QueryRewriter
from src.utils.env_loader import load_env


class MyRetriever:
    """
        A custom retriever that combines query rewriting, searcher, and reranker retrieved documents.
    """
    def __init__(self, query: str, searcher: QdrantSearchBGE, query_rewriter: QueryRewriter,
                 reranker: Reranker, k: int = 5):
        self.searcher = searcher
        self.query_rewriter = query_rewriter
        self.reranker = reranker
        self.k = k
        self.query = query

    def get_relevant_documents(self, query) -> List[Document]:
        """
        Retrieve relevant documents given a query.
        Args:
            query (str): The original user query.
        Returns:
            List[Document]: Reranked list of relevant documents.
        """
        # Rewrite original query
        query = self.query
        rewritten_query = self.query_rewriter.rewrite_query(query)
        print(f"Rewritten query: {rewritten_query}")
        logger.info(f"Rewritten query: {rewritten_query}")

        # Retrieve candidate documents
        relevant_documents = self.searcher.search(query_text=rewritten_query, limit=self.k)
        for idx, doc in enumerate(relevant_documents, start=1):
            logger.info(f"Relevant doc {idx}: {doc}")

        formatted_relevant_documents = [doc.payload['text'] for doc in relevant_documents]

        # Rerank candidate documents
        reranked_documents = self.reranker.rerank_documents(rewritten_query, formatted_relevant_documents)
        # for idx, doc in enumerate(reranked_documents, start=1):
        #     logger.info(f"Reranked doc {idx}: {doc}")

        return reranked_documents

# if __name__ == "__main__":
#     load_env("local")
#     searcher = QdrantSearchBGE(collection_name="diseases_collection", embedding_model_name="BAAI/bge-m3",
#                                use_fp16=False)
#
#     query_rewriter = QueryRewriter(model="meta-llama/Llama-3-8b-chat-hf", max_tokens=200, temperature=0.1)
#     reranker = Reranker()
#
#     retriever = MyRetriever(searcher=searcher, query_rewriter=query_rewriter, reranker=reranker, k=5)
#
#     example_query = """Các triệu chứng của bệnh tiểu đường là gì?"""
#     documents = retriever.get_relevant_documents(example_query)
