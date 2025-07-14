import streamlit as st

from src.database.qdrant.config import get_qdrant_client
from src.utils.env_loader import load_env


load_env("local")

st.set_page_config(page_title="ChocoHunter Chat", page_icon="/assets/chocolate_icon.png")

# Add custom CSS for button text color, session list, and delete button
st.markdown("""
    <style>
    .stButton > button {
        color: #FFFFFF;
        background-color: #4CAF50;
        border: none;
        padding: 8px 16px;
        border-radius: 5px;
        width: 100%;
        text-align: left;
    }
    .stButton > button:hover {
        color: #FFFFFF;
        background-color: #45a049;
    }
    .thinking {
        color: #888;
        font-style: italic;
    }
    .session-button {
        margin-bottom: 5px;
    }
    .delete-button {
        color: #FFFFFF;
        background-color: #FF4444;
        border: none;
        padding: 5px 10px;
        border-radius: 5px;
        margin-left: 10px;
        font-size: 12px;
    }
    .delete-button:hover {
        background-color: #CC0000;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize database
qdrant_client = get_qdrant_client()


# Initialize messages
# if "messages" not in st.session_state:
#     if st.session_state.current_session_id and st.session_state.current_session_id in st.session_state.sessions:
#         st.session_state.messages = st.session_state.sessions[st.session_state.current_session_id]["messages"]
#     else:
#         st.session_state.messages = []

# Display chat history
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])


# Sidebar
st.sidebar.header("ChocoHunter Chatbot")

# New conversation
if st.sidebar.button("Trò chuyện mới"):
    st.rerun()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

for message in st.session_state.chat_history:
    st.chat_message(message["role"]).markdown(message["content"])

# User input
if prompt := st.chat_input("Send a message"):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    assistant_response_generator = [character for character in f"Echo: {prompt}"]
    response = st.chat_message("assistant").write_stream(assistant_response_generator)
    st.session_state.chat_history.append({"role": "assistant", "content": response})


# # Display recent sessions sorted by timestamp
# st.sidebar.subheader("Lịch sử trò chuyện")
# recent_sessions = sorted(st.session_state.sessions.items(), key=lambda x: x[1]["timestamp"], reverse=True)
# for session_id, session_data in recent_sessions:
#     timestamp = session_data["timestamp"].strftime("%d/%m/%Y %H:%M")
#     col1, col2 = st.sidebar.columns([3, 1])
#     with col1:
#         if st.button(f"Session {session_id[:8]} - {timestamp}", key=f"session_{session_id}", help="Nhấn để tải lại phiên này"):
#             st.session_state.current_session_id = session_id
#             st.session_state.messages = st.session_state.sessions[session_id]["messages"]
#             # logger.info(f"Switched to session: {session_id}")
#             st.rerun()
#     with col2:
#         if st.button("🗑️", key=f"delete_{session_id}", type="primary"):
#             # delete_session(session_id)
#             del st.session_state.sessions[session_id]
#             if st.session_state.current_session_id == session_id:
#                 if st.session_state.sessions:
#                     recent_session = max(st.session_state.sessions.items(), key=lambda x: x[1]["timestamp"])
#                     st.session_state.current_session_id = recent_session[0]
#                     st.session_state.messages = st.session_state.sessions[recent_session[0]]["messages"]
#                 else:
#                     st.session_state.current_session_id = None
#                     st.session_state.messages = []
#             # logger.info(f"Deleted session: {session_id}")
#             st.rerun()
