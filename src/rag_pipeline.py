from src.database.qdrant.qdrant_search import QdrantSearchBGE
from src.generator import Generator
from src.reranker import Reranker
from src.retriever import MyRetriever
from src.rewrite_query import QueryRewriter
from src.utils.env_loader import load_env


class RAGPipeline:
    def __init__(self, query, retriever, generator):
        self.query = query
        self.retriever = retriever
        self.generator = generator

    def run(self):
        # Retrieve relevant documents
        documents = self.retriever.get_relevant_documents(self.query)

        # Generate an answer
        final_answer = self.generator.generate_answer(self.query, documents)

        return final_answer

# if __name__ == '__main__':
#     load_env("local")
#     example_query = "Thủ đô của Việt Nam ở đâu?"
#     query_rewriter = QueryRewriter(example_query)
#     searcher = QdrantSearchBGE(collection_name="diseases_collection", embedding_model_name="BAAI/bge-m3")
#     documents = searcher.search(example_query)
#     print(documents)
#     print(type(documents))
#     reranker = Reranker(model_name="BAAI/bge-reranker-v2-m3", document_list=documents)
#     retriever = MyRetriever(query=example_query, searcher=searcher,
#                             query_rewriter=query_rewriter,reranker=reranker,k=5)
#     generator = Generator()
#     rag= RAGPipeline(query=example_query, retriever=retriever, generator=generator)
#     answer = rag.run()
#     print("Answer:", answer)
