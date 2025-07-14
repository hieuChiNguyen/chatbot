import streamlit as st

st.header("ChocoHunter Chat")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    st.chat_message(message["role"]).markdown(message["content"])

if prompt := st.chat_input("Send a message"):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    assistant_response_generator = [character for character in f"Echo: {prompt}"]
    response = st.chat_message("assistant").write_stream(assistant_response_generator)
    st.session_state.chat_history.append({"role": "assistant", "content": response})