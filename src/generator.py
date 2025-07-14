from typing import List

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_together import ChatTogether

from src.utils.env_loader import load_env


class Generator:
    def __init__(self, model_name: str = "meta-llama/Llama-3-8b-chat-hf"):
        self.model_name = model_name
        self.llm = ChatTogether(
            model=self.model_name,
        )

        # Define the prompt template for RAG
        self.prompt_template = ChatPromptTemplate.from_template(
            """
                You are a helpful assistant. Based on the following context, provide a concise and accurate answer to the question.
                Context: {context}
                Question: {question}
                Answer: 
            """
        )

    def generate_answer(self, query: str, relevant_docs: List[Document]):
        context = " ".join(
            [doc.payload['text'] if hasattr(doc, 'payload') and 'text' in doc.payload else doc
             for doc in relevant_docs]
        )
        print(f"Context: {context}")

        # Create the prompt
        prompt = self.prompt_template.format(context=context, question=query)
        print(f"Prompt: {prompt}")

        # Generate the answer
        response = self.llm.invoke(prompt)
        return response


# if __name__ == "__main__":
#     load_env("local")
#     # Initialize the generator
#     generator = Generator()
#
#     re_query = "Thủ đô của Việt Nam là gì?"
#     relevant_documents = [
#         "Thủ đô của Việt Nam là Hà Nội.",
#         "Hà Nội là trung tâm chính trị và văn hóa của Việt Nam.",
#         "Việt Nam có thủ đô nằm ở miền Bắc."
#     ]
#
#     answer = generator.generate_answer(re_query, relevant_documents)
#     print("Answer:", answer)
