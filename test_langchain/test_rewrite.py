# Rewrite Retrieval Read: langchain-ai/rewrite
import os
import sys

from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_together import ChatTogether
from langsmith import Client

from src.utils import load_env

load_env("local")

print(sys.path[0])

client = Client(api_key=os.getenv("LANGCHAIN_API_KEY"))
print("client: ", client)

# Pull the prompt definition
prompt = client.pull_prompt("langchain-ai/rewrite", include_model=True)
"""
Provide a better search query for web search engine to answer the given question, end the queries 
with ’**’.  Question {x} Answer:
"""
# Bản thân prompt đã là 1 PromptTemplate rồi => Không cần ChatPromptTemplate
print("prompt: ", prompt)
# print(f"prompt template ({type(prompt.template).__name__}): {
# prompt.template}")
# template='Provide a better search query for web search engine to answer the
# given question, end the queries with
# ’**’.  Question {x} Answer:
# x -> placeholder

llm = ChatTogether(
    model="meta-llama/Llama-3-8b-chat-hf",
    max_tokens=200,
    temperature=0.2
)

# Create a runnable sequence: input -> prompt -> llm -> output
rewrite_runnable = {
                       "x": RunnablePassthrough()
                       # Assumes the prompt expects 'x' as input
                   } | prompt | llm | RunnableLambda(lambda x: x.content)

print("rewrite:: ", rewrite_runnable)

# The langchain-ai/rewrite prompt typically expects 'x' as input.

original_query = """Who is the lead actor in the movie 'Inception' and what 
year was it released?"""

rewritten_query = rewrite_runnable.invoke(original_query)

print(f"Original Query: {original_query}")
print(f"Rewritten Query: {rewritten_query}")

# Test rewrite runnable sequence đơn giản hơn
# chain = prompt | llm
# chain = prompt | llm | RunnableLambda(lambda x: x.content)
#
# original_query = (
#     """Who is the lead actor in the movie 'Inception' and what year was it
#     released?""")
# result = chain.invoke({"x": original_query})
# print(result)

"""
Giải thích từng thành phần:
+ rewrite_runnable: Đây là tên của chuỗi xử lý (runnable sequence) được tạo 
ra. Nó là một chuỗi các bước xử lý được  liên kết với nhau, nhận đầu vào (
input), xử lý qua các bước, và trả về đầu ra  (output).
+ {"x": RunnablePassthrough()}: "x": Đây là một từ khóa (key) trong một 
dictionary, đại diện cho tên biến đầu vào mà  prompt mong đợi. Theo metadata 
của prompt bạn cung cấp trước đó ( input_variables=['x']), prompt sử dụng 
biến x để chứa giá trị của truy vấn gốc (original query).
+ RunnablePassthrough(): Đây là một đối tượng trong LangChain, có nhiệm vụ 
chuyển tiếp đầu vào mà không thay đổi nó.  Nghĩa là bất kỳ dữ liệu đầu vào 
nào được cung cấp (ví dụ: chuỗi truy vấn gốc) sẽ được gán trực tiếp vào biến 
x mà không bị sửa đổi. Ý nghĩa: Phần này đảm bảo rằng truy vấn gốc (ví dụ: 
"Who is the lead actor in the movie 'Inception' and what year was it 
released?") được truyền vào prompt dưới dạng biến x.
+ | (Pipe Operator):
Trong LangChain, toán tử | được sử dụng để liên kết các bước trong một chuỗi 
xử lý. Nó giống như việc nói "lấy đầu ra của bước trước và đưa nó vào bước 
tiếp theo".
+ llm là "bộ não" xử lý ngôn ngữ tự nhiên, thực hiện nhiệm vụ viết lại truy vấn 
dựa trên lời nhắc được cung cấp.
+ RunnableLambda(lambda x: x.content):
RunnableLambda: Đây là một công cụ trong LangChain cho phép bạn định nghĩa 
một hàm tùy chỉnh (custom function) để xử 
lý đầu ra của bước trước đó (ở đây là đầu ra của LLM). 
lambda x: x.content: Đây là một hàm lambda nhận đầu vào x (đầu ra của LLM) và 
trích xuất thuộc tính content từ nó. Đầu ra của LLM thường là một đối tượng 
phức tạp (ví dụ: một đối tượng ChatMessage hoặc tương tự), nhưng bạn chỉ muốn 
lấy phần nội dung văn bản (text content) của phản hồi.
Ý nghĩa: Phần này đảm bảo rằng đầu ra cuối cùng của chuỗi là một chuỗi văn bản 
thuần túy, thay vì một đối tượng phức tạp.

Tóm tắt luồng xử lý:
1. Đầu vào: Truy vấn gốc (original query) được đưa vào chuỗi, ví dụ: "Who is 
the lead actor in the movie 'Inception' and what year was it released?".
2. RunnablePassthrough: Chuyển truy vấn gốc vào biến x.
3. prompt: Biến x được điền vào template của prompt để tạo lời nhắc hoàn chỉnh 
gửi đến LLM.
4. llm: LLM xử lý lời nhắc và tạo ra một truy vấn được viết lại (rewritten 
query).
5. RunnableLambda: Trích xuất nội dung văn bản từ đầu ra của LLM.
6. Đầu ra: Kết quả cuối cùng là một chuỗi văn bản, ví dụ: "Lead actor Inception 
movie release year **".
"""
