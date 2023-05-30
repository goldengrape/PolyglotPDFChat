import streamlit as st
from streamlit_server_state import server_state, server_state_lock
from polyglotPDFChat import ChatApplication,Participant
from layout import draw_layout
from control_flow import (
    init_sessions,
    gather_user_info,
    create_or_join_room,
    input_message,
    output_message)

init_sessions()
layout=draw_layout()
user=gather_user_info(
    layout["user_setting"],
    layout["stream_box"],
    layout["speak_box"])

room=create_or_join_room(layout["room_setting"])

# track and test
# if user:
#     st.markdown(f"current user: {user}")
# if room:
#     st.markdown(f"current chat room: {room.name}")
#     st.markdown(f"* speaker: {room.speaker.name}")
#     st.markdown(f"* listeners: {room.listeners}")

# with server_state_lock["chat_messages"]:
#     if "chat_messages" not in server_state:
#         server_state["chat_messages"] = {}

input_message(
    layout["message_input"],
    room,
    user)

output_message(
    layout["message_output"],
    room)