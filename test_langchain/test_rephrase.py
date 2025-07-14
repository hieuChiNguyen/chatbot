from langchain_huggingface import HuggingFaceEmbeddings
from langchain.retrievers import RePhraseQueryRetriever
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_together import ChatTogether


# Initialize embeddings for vector store
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create a sample vector store (replace with your actual vector store)
documents = [
    """California offers various treatment programs for alcoholism and drug 
    abuse, including inpatient and outpatient rehab centers.""",
    """Inpatient treatment programs in California provide 24/7 care for 
    severe addiction cases.""",
    """Outpatient programs in California allow patients to attend therapy 
    sessions while living at home.""",
    """Many treatment centers in California are located in Los Angeles and 
    San Francisco."""
]
vectorstore = FAISS.from_texts(documents, embeddings)

# Define retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# Define rephrase prompt
# Custom prompt for rephrasing queries
rephrase_prompt = ChatPromptTemplate.from_template(
    """Provide a better search query for web search engine to answer the given question. Provide 
    only the rephrased question.

    Original question: {query}

    Rephrased question:"""
)

llm = ChatTogether(
    model="meta-llama/Llama-3-8b-chat-hf",
    max_tokens=200,
    temperature=0.2
)

# Create LLM chain for rephrasing
llm_chain = (
        {"query": RunnablePassthrough()} |
        rephrase_prompt |
        llm |
        RunnableLambda(lambda x: x.content)
)

# Create RePhraseQueryRetriever
retriever_from_llm_chain = RePhraseQueryRetriever(
    retriever=retriever,
    llm_chain=llm_chain
)

original_query = ("""What are treatment programs for alcoholism and drug 
                    abuse in California?""")

rephrased_query = llm_chain.invoke(original_query)
print(f"Rephrased Query: {rephrased_query}")

# Invoke the retriever
results = retriever_from_llm_chain.invoke(original_query)

print("Retrieved Documents:")
for i, doc in enumerate(results, 1):
    print(f"Document {i}: {doc.page_content}")
