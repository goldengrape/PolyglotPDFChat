import streamlit as st
from streamlit_server_state import server_state, server_state_lock
from polyglotPDFChat import ChatApplication,Participant
from layout import draw_layout
from control_flow import (
    init_sessions,
    gather_user_info,
    create_or_join_room,
    input_message,
    output_message,
    ai_setting)

init_sessions()
layout=draw_layout()

ai_setting(layout["ai_setting"])

user=gather_user_info(
    layout["user_setting"],
    layout["stream_box"],
    layout["speak_box"])

room=create_or_join_room(layout["room_setting"])

input_message(
    layout["message_input"],
    room,
    user)

output_message(
    layout["message_output"],
    room)