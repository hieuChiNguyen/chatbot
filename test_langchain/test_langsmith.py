import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_together import Together
from langchain_core.tracers.context import tracing_v2_enabled
from dotenv import load_dotenv
from langsmith import traceable

# Thiết lập biến môi trường (nếu chưa thiết lập)
load_dotenv()
os.environ["TOGETHER_API_KEY"] = os.getenv("TOGETHER_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")


# Khởi tạo mô hình từ Together AI
llm = Together(
    model="meta-llama/Llama-3-8b-chat-hf",
    max_tokens=200,
    temperature=0.2
)

# # Tạo prompt template
# prompt = ChatPromptTemplate.from_template(
#     "Viết một đoạn văn ngắn về {topic} bằng tiếng Việt."
# )

# Tạo ChatPromptTemplate với nhiều loại template
prompt = ChatPromptTemplate.from_messages([
    # System message: Cung cấp ngữ cảnh và vai trò của AI
    ("system", "Bạn là một trợ lý AI chuyên viết nội dung bằng tiếng Việt với giọng điệu chuyên nghiệp và súc tích. Hãy đảm bảo đoạn văn ngắn gọn, dưới 100 từ, và sử dụng ngôn ngữ tự nhiên."),
    # Human message: Yêu cầu từ người dùng với placeholder động
    ("human", "Viết một đoạn văn ngắn về {topic} bằng tiếng Việt, tập trung vào lợi ích chính của nó."),
    # Assistant message (tùy chọn): Định dạng một phần phản hồi trước, nếu cần
    ("assistant", "Dưới đây là đoạn văn về {topic}:")
])

print("prompt: ", prompt)

# Tạo chain
chain = prompt | llm | StrOutputParser()
print("chain: ", chain)

# Chạy chain với LangSmith tracing

# with tracing_v2_enabled(project_name="TogetherAI-LangSmith-Integration"):
response = chain.invoke({"topic": "tầm quan trọng của học máy"})

print(response)

# The above chain will be traced as a child run of the traceable function
# @traceable(
#     tags=["openai", "chat"],
#     metadata={"foo": "bar"}
# )
# def invoke_runnnable(question, context):
#     result = chain.invoke({"question": question, "context": context})
#     return "The response is: " + result
#
# invoke_runnnable("Can you summarize this morning's meetings?", "During this morning's meeting, we solved all world conflict.")