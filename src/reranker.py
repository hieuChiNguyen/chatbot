import os

import cohere
from FlagEmbedding import FlagReranker

from logger import logger
from src.utils.env_loader import load_env


class Reranker:
    def __init__(self, model_name="BAAI/bge-reranker-v2-m3", document_list=None):
        self.model_name = model_name
        if self.model_name == "cohere":
            self.reranker = get_cohere_client()
        else:
            self.reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=False)

        self.document_list = document_list

    def rerank_documents(self, query, document_list):
        """
            Rank the documents based on the query;
            query: str
            document_list: List[Document]
        """
        if not all(isinstance(doc, str) for doc in document_list):
            self.document_list = [doc.payload['text'] for doc in document_list]

        self.document_list = document_list

        if self.model_name == "cohere":
            reranker_results = self.reranker.rerank(
                query=query, documents=self.document_list,
                top_n=5,
                model="rerank-multilingual-v3.0"
            ).results

            relevance_score = [result.relevance_score for result in reranker_results]
            logger.info(f"reranked_score: {relevance_score}")
            reranked_documents = [document_list[result.index] for result in reranker_results]
            return reranked_documents


        else:
            reranked_score = self.reranker.compute_score(
                [(query, document) for document in self.document_list],
                normalize=True
            )
            logger.info(f"reranked_score: {reranked_score}")
            # sort the documents based on the reranked_score
            reranked_documents = [document for _, document in
                                 sorted(zip(reranked_score, self.document_list), reverse=True)]
            return reranked_documents

def get_cohere_client():
    load_env("local")
    cohere_api_key = os.getenv("COHERE_API_KEY")
    cohere_client = cohere.Client(cohere_api_key)
    return cohere_client

# if __name__ == "__main__":
#     load_env("local")
#     # rerank = Rerank()
#     example_query = "Thủ đô"
#     document_list = ["trung tâm", "capital", "kinh đô"]
#     rerank = Reranker()
#     reranked_document_list = rerank.rerank_documents(example_query, document_list)
#     print("reranked_document_list:", reranked_document_list)
