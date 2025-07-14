import streamlit as st

# Sidebar card for file upload functionality
def upload_sidebar():
    st.page_link("upload.py", label="Upload your files", icon=":material/dashboard:")
    a,b,c = st.tabs(["Tab A", "Tab B", "Tab C"])
    a.write("Tab A content")
    b.write("Tab B content")
    c.write("Tab C content")
    st.expander("Expander").write("Expander content")
    st.popover("Popover", icon=":material/info:").write("Popover content")

# Sidebar card for chat functionality
def chat_sidebar():
    # Thêm CSS
    st.markdown("""
        <style>
        div.stButton > button:hover {
            color: #1E90FF;
            border-color: #1E90FF;
        }
        </style>
    """, unsafe_allow_html=True)

    st.button("Trò chuyện mới", type="secondary")



