import streamlit as st
from streamlit_server_state import server_state

def draw_layout():
    layout={  
        "ai_setting":st.expander("AI Setting"),
        "user_setting":st.expander("User Setting",
                    expanded=(st.session_state["user"] is None)),
        "room_setting":st.expander("Lecture Hall Setting",
                    expanded=(st.session_state["room"] is None)),
        "PDF_display":st.empty(),
        "PDF_play_control":st.empty(),
        "message_input":st.empty(),
        "stream_box":st.empty(),
        "speak_box":st.empty(),
        "message_output":st.container(),
        "history_box":st.empty(),
    }
    return layout 

if __name__ == "__main__":
    layout=draw_layout(),



