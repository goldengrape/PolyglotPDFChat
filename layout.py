import streamlit as st

def draw_layout():
    layout={  
        "ai_setting":st.expander("AI Setting"),
        "user_setting":st.expander("User Setting",expanded=True),
        "room_setting":st.expander("Room Setting"),
        "PDF_display":st.empty(),
        "PDF_play_control":st.empty(),
        "message_input":st.empty(),
        "stream_box":st.empty(),
        "speak_box":st.empty(),
        "message_output":st.empty(),
        "history_box":st.empty(),
    }
    return layout 

if __name__ == "__main__":
    layout=draw_layout(),



