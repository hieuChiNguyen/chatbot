import streamlit as st

from sidebar import (
    chat_sidebar
)

if "init" not in st.session_state:
    st.session_state.init = True


pages = [
    st.Page(
        "home.py",
        title="Trang chủ",
        icon=":material/home:"
    ),
    st.Page(
        "upload.py",
        title="Tải tệp lên",
        icon=":material/upload:"
    ),
    st.Page(
        "chat.py",
        title="Trò chuyện",
        icon=":material/chat:"
    ),
]

page = st.navigation(pages)
page.run()

with st.sidebar:
    if page.title == "Trang chủ":
        st.page_link("home.py", label="Trang chủ", icon=":material/home:")
        st.write("Chào mừng đến ChocoHunter")

    if page.title == "Trò chuyện":
        chat_sidebar()

    # if page.title == "Upload Files":
    #     upload_card()
    # elif page.title == "Chat":
    #     chat_card()
    # else:
    #     st.page_link("home.py", label="Home", icon=":material/home:")
    #     st.write("Welcome to the home page!")

# st.sidebar.caption(
#     "ChocoHunter License"
# )
