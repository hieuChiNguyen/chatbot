# ChocoHunter-Chat: Build a medical chatbot using RAG pipeline

## Nội dung

- [1. Giới thiệu](#1-giới-thiệu)
    - [1.1. Tổng quan](#11-tổng-quan)
    - [1.2. Mục tiêu](#12-mục-tiêu)
- [2. Tổng hợp kiến thức](#2-tổng-hợp-kiến-thức)
    - [2.1. Together AI](#21-together-ai)
    - [2.2. RAG](#22-rag)
    - [2.3. LangChain](#23-langchain)
- [3. Cài đặt và cấu hình](#3-cài-đặt-và-cấu-hình)
    - [3.1. Cài đặt thư viện](#31-cài-đặt-thư-viện)
    - [3.2. File .env](#32-file-env)
    - [3.3. Các biến môi trường](#33-các-biến-môi-trường)
- [4. Câu hỏi thường gặp](#4-câu-hỏi-thường-gặp)
- [5. Đóng góp](#5-đóng-góp)
- [6. Giấy phép](#6-giấy-phép)

## 1. Giới thiệu

## 2. Tổng hợp kiến thức

### 2.1. Together AI

- Together AI là một nền tảng đám mây (AI Acceleration Cloud) cung cấp các dịch vụ trí tuệ nhân tạo tập trung vào việc
  chạy, tinh chỉnh và huấn luyện các mô hình AI tạo sinh (generative AI) với hiệu suất cao và chi phí tối ưu.
  Nền tảng này cung cấp các API dễ sử dụng và cơ sở hạ tầng GPU có khả năng mở rộng, hỗ trợ các nhà phát triển, doanh
  nghiệp và nhà nghiên cứu triển khai các mô hình AI một cách hiệu quả.
- together: Là thư viện chính thức của Together AI, cung cấp quyền truy cập đầy đủ vào các API của họ, phù hợp cho các
  dự án cần tính linh hoạt và không phụ thuộc vào LangChain.
- langchain-together: Là gói tích hợp để sử dụng Together AI trong hệ sinh thái LangChain.

### 2.2. RAG

- RAG (Retrieval-Augmented Generation) là một phương pháp kết hợp giữa truy xuất thông tin và sinh văn bản, cho phép các
mô hình AI tạo ra câu trả lời chính xác hơn bằng cách truy xuất thông tin từ các nguồn dữ liệu bên ngoài.

### 2.3. LangChain

- LangChain là một framework mã nguồn mở giúp xây dựng các ứng dụng AI phức tạp bằng cách kết hợp các mô-đun khác nhau
như truy xuất dữ liệu, xử lý ngôn ngữ tự nhiên và tương tác với người dùng. Nó cung cấp các công cụ và API để dễ dàng 
tích hợp các mô hình AI, cơ sở dữ liệu và giao diện người dùng.


## 3. Cài đặt
