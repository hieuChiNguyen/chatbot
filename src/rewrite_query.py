from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_together import ChatTogether

# from src.utils.env_loader import load_env


class QueryRewriter:
    SUPPORTED_MODELS = [
        "meta-llama/Llama-3-8b-chat-hf",
        "meta-llama/Llama-3-70b-chat-hf",
        "mistralai/Mixtral-8x7B-Instruct-v0.1",
    ]

    def __init__(self, model="meta-llama/Llama-3-8b-chat-hf", max_tokens=200, temperature=0.1):
        # Check model exists in SUPPORTED_MODELS, if not use default model
        self.model = model if model in self.SUPPORTED_MODELS else self.SUPPORTED_MODELS[0]
        self.max_tokens = max_tokens
        self.temperature = temperature

        # Init prompt template
        # rewrite_prompt = """Provide a better search query for web search engine to answer the given
        #     question, end the queries with ’**’.  Question {query} Answer:"""
        rewrite_prompt = """Rewrite the following question: {query} to a better search query
        for web search engine to answer. Return ONLY the rewritten query. Do NOT provide 
        explanations, answers, or additional information."""
        self.rewrite_template = ChatPromptTemplate.from_template(rewrite_prompt)

        # Init LLM
        self.llm = ChatTogether(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature
        )

        # Tạo runnable sequence: input -> prompt -> llm -> output
        self.rewrite_chain = (
                {"query": RunnablePassthrough()} |
                self.rewrite_template |
                self.llm |
                RunnableLambda(lambda x: x.content)
        )

    def rewrite_query(self, origin_query: str):
        """
        Hàm trả về original_query và rewritten_query.
        Args:
            origin_query (str)
        Returns:
            rewritten_query (str)
        """
        # rewritten_query = self.rewrite_chain.invoke(origin_query)
        # return origin_query, rewritten_query
        rewritten_query = self.rewrite_chain.invoke(origin_query)
        return rewritten_query

    def get_supported_models(self):
        """
        Returns:
            list: List supported models.
        """
        return self.SUPPORTED_MODELS

    def check_complex_query(self, query: str) -> bool:
        return False

# if __name__ == "__main__":
#     # Khởi tạo với model cụ thể
#     load_env("local")  # Load environment variables if needed
#     rewriter = QueryRewriter(model="meta-llama/Llama-3-8b-chat-hf")
#     print("Selected model:", rewriter.model)
#
#     # query = "Who is the lead actor in the movie 'Inception' and what year was it released?"
#     query = "What is the capital city of Japan and how many people live there?"
#     original_query, rewritten_query = rewriter.rewrite_query(query)
#
#     print(f"Original Query: {original_query}")
#     print(f"Rewritten Query: {rewritten_query}")
