import streamlit as st
from polyglotPDFChat import (
    Participant,ChatApplication,
    )
from streamlit_server_state import (
    server_state, server_state_lock,
    force_rerun_bound_sessions,
)
import os 


def init_session_state(key,value):
    if key not in st.session_state:
        st.session_state[key]=value

def init_server_state(key,value):
    with server_state_lock[key]:
        if key not in server_state:
            server_state[key] = value

def init_sessions():
    # server_state
    # init_server_state("chat_messages",{})
    # init_server_state("room",None)

    # session_state
    init_session_state("first_run",True)
    init_session_state("user",None)
    init_session_state("room",None)
    init_session_state("speaker_said_that",None)

    if st.session_state["first_run"]:
        init_server_state("chatApp",ChatApplication())
        st.session_state["first_run"]=False

    


def gather_user_info(container, stream_box, speak_box):
    if st.session_state["user"] is not None:
        return st.session_state["user"]
    
    # User inputs their name and role
    form=container.form("user_info")
    with form:
        name = form.text_input("name", key="name")
        role = form.selectbox("Role", ["speaker", "listener"], key="role")

        # User inputs their language and voice settings
        language = form.selectbox("Language", ["English", "Chinese"], key="language")
        voice = form.selectbox("Voice", [
            "en-US-AriaNeural",
            "en-US-GuyNeural",
            "zh-CN-XiaoxiaoNeural",
            "zh-CN-YunyangNeural",
            ], 
            key="voice")
        speed_num = form.slider("Voice Speed", min_value=0.5, max_value=2.0, step=0.1, key="speed", value=1.0)
        speed = f"{(speed_num-1)*100:.2f}%"

        if st.secrets.get("openai_api_key",False) and \
            st.secrets.get("speech_key",False) and \
            st.secrets.get("speech_region",False) and \
            st.secrets.get("run_place",False):
            
            openai_key = st.secrets["openai_api_key"]
            speech_key = st.secrets["speech_key"]
            speech_region = st.secrets["speech_region"]
            run_place=st.secrets["run_place"]
        else:
            openai_key = form.text_input("OpenAI API Key",     
                    value="", type="password")
            speech_key=form.text_input("Azure Speech Key", 
                    value="",  type="password")
            speech_region=form.text_input("Azure Speech Region",
                    value="westus")
            run_place="cloud"
        submitted = form.form_submit_button("Submit")
    if submitted:
        submitted=False
        user=Participant(
            name=name, 
            role=role, 
            language=language, 
            voice=voice, 
            speed=speed, 
            stream_box=stream_box, 
            speak_box=speak_box,
            speak=(role=="listener"),
            openai_key=openai_key,
            speech_key=speech_key,
            speech_region=speech_region,
            run_place=run_place)
        st.session_state["user"]=user
    return st.session_state["user"] 

def create_or_join_room(container):
    if st.session_state["user"] is None:
        return None
    
    form=container.form("Lecture Hall") 
    with form:
        if st.session_state["user"].role== "speaker":
            room_name = form.text_input("Create a new Lecture Hall", key="room_name")
        else:
            room_name = form.selectbox(
                "Join a room", 
                server_state["chatApp"].display_rooms(), 
                key="room_name")
        submitted = form.form_submit_button("Submit")
    if submitted:
        submitted=False
        if st.session_state["user"].role== "speaker":
            with server_state_lock["chatApp"]:
                server_state["chatApp"].create_room(
                    room_name, 
                    st.session_state["user"])  # Ensure this is a Participant instance, not a string.
            # with server_state_lock["chat_messages"]:
            #     server_state["chat_messages"][room_name]=[]
            form.success("You created a new Lecture Hall")
        else:
            with server_state_lock["chatApp"]:
                server_state["chatApp"].add_listener_to_room(
                    room_name, 
                    st.session_state["user"])  # Ensure this is a Participant instance, not a string.
            form.success("You joined a Lecture Hall")
        # with server_state_lock["room"]:
        st.session_state["room"]=server_state["chatApp"].rooms[room_name]
    return st.session_state["room"]

def on_message_input(room_name, participant):
    if room_name and participant:
        new_message_text = st.session_state["message_input"]
        if not new_message_text:
            return

        with server_state_lock["chatApp"]:
            server_state["chatApp"].rooms[room_name].add_message(
                st.session_state["user"], 
                new_message_text)
        force_rerun_bound_sessions("chatApp")

def input_message(container,room,participant):
    if room is None:
        return 
    
    container.text_input("Message", key="message_input", on_change=on_message_input, args=(room.name, participant))

def output_message(container,room):

    if st.session_state["room"] is None:
        return
    speaker_message=st.session_state["room"].speaker_last_message()
    listener_message=st.session_state["room"].export_messages(display_role=["listener"])
    if speaker_message != st.session_state["speaker_said_that"]:
        translated_message=st.session_state["user"].receive_message(speaker_message)
        st.session_state["speaker_said_that"]=speaker_message
    else:
        translated_message=st.session_state["speaker_said_that"]
    
    
    container.markdown(" Speakers said:")
    container.markdown(translated_message)
    container.markdown(" Listeners said:")
    container.markdown(listener_message)


def ai_setting(c):
    if st.secrets.get("openai_api_key") and st.secrets.get("speech_key") and st.secrets.get("speech_region"):
        os.environ["OPENAI_API_KEY"] = st.secrets.get("openai_api_key")
        os.environ['SPEECH_KEY'] = st.secrets.get("speech_key")
        os.environ['SPEECH_REGION'] = st.secrets.get("speech_region")
        return 
    if os.environ.get("OPENAI_API_KEY",False) and \
        os.environ.get('SPEECH_KEY',False) and \
        os.environ.get('SPEECH_REGION',False):
        return

    form=c.form("AI Setting")
    with form:
        openai_key = form.text_input("OpenAI API Key",     
                value="", type="password")
        speech_key=form.text_input("Azure Speech Key", 
                value="",  type="password")
        speech_region=form.text_input("Azure Speech Region",
                value="westus")
        submitted = form.form_submit_button("Submit")
    if submitted:
        os.environ["OPENAI_API_KEY"] = openai_key
        os.environ['SPEECH_KEY']=speech_key
        os.environ['SPEECH_REGION']=speech_region


    

