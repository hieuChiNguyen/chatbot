import streamlit as st

from cards import (
    upload_card,
    chat_card
)

st.title("ChocoHunter AI")

st.markdown(
    """Ứng dụng AI Chatbot cho các dịch vụ y tế và chăm sóc sức khỏe."""
)

cols = st.columns(2)

with cols[1].container(height=310):
    upload_card()
with cols[0].container(height=310):
    chat_card()
