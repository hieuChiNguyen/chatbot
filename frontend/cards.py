import streamlit as st

# Home card for file upload functionality
def upload_card():
    st.page_link("upload.py", label="Tải lên tệp của bạn", icon=":material/dashboard:")
    a,b,c = st.tabs(["Tab A", "Tab B", "Tab C"])
    a.write("Tab A content")
    b.write("Tab B content")
    c.write("Tab C content")
    st.expander("Expander").write("Expander content")
    st.popover("Popover", icon=":material/info:").write("Popover content")

# Home card for chat functionality
def chat_card():
    st.page_link("chat.py", label="Lịch sử trò chuyện", icon=":material/chat:")
    st.chat_message("user").write("Xin chào bạn")
    st.chat_message("assistant").write("Rất vui được giải đáp")
    st.chat_input("Type something")
