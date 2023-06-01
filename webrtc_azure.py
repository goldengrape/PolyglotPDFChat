import os
import io
import streamlit as st
import numpy as np
from streamlit_webrtc import WebRtcMode, webrtc_streamer
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioDataStream, AudioConfig
from azure.cognitiveservices.speech import ResultReason, CancellationReason
from azure.cognitiveservices.speech.audio import PullAudioInputStreamCallback, PullAudioInputStream
import queue

class AudioBuffer:
    def __init__(self):
        self.buffer = queue.Queue()

    def write(self, data):
        self.buffer.put(data)

    def readinto(self, buf):
        try:
            data = self.buffer.get(block=False)
            buf[:len(data)] = data
            return len(data)
        except queue.Empty:
            return 0

class MyPullAudioInputStreamCallback(PullAudioInputStreamCallback):
    def __init__(self, audio_buffer):
        super().__init__()
        self.audio_buffer = audio_buffer

    def read(self, buffer):
        return self.audio_buffer.readinto(buffer)

    def close(self):
        pass



def app_sst(
        status_indicator,
        text_output,
        timeout=3
        ):
    speech_key = os.environ["SPEECH_KEY"]
    speech_region = os.environ["SPEECH_REGION"]

    audio_buffer = AudioBuffer()
    callback = MyPullAudioInputStreamCallback(audio_buffer)
    audio_input_stream = PullAudioInputStream(callback)
    audio_output = AudioConfig(stream=audio_input_stream)
    speech_config = SpeechConfig(subscription=speech_key, region=speech_region)
    speech_recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_output)

    webrtc_ctx = webrtc_streamer(
        key="speech-to-text",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        media_stream_constraints={"video": False, "audio": True},
    )

    while True:
        if webrtc_ctx.audio_receiver:
            status_indicator.write("Running. Say something!")

            try:
                audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=timeout)
                for audio_frame in audio_frames:
                    audio_buffer.write(audio_frame.to_ndarray().tobytes())
                result = speech_recognizer.recognize_once_async().get()
                if result.reason == ResultReason.RecognizedSpeech:
                    text_output.write(result.text)
                elif result.reason == ResultReason.NoMatch:
                    text_output.write("No speech could be recognized.")
                elif result.reason == ResultReason.Canceled:
                    cancellation_details = result.cancellation_details
                    text_output.write(f"Speech Recognition canceled: {cancellation_details.reason}")
                    if cancellation_details.reason == CancellationReason.Error:
                        text_output.write(f"Error details: {cancellation_details.error_details}")
            except queue.Empty:
                status_indicator.write("No frame arrived.")
        else:
            status_indicator.write("Stopping.")
            break


def main():
    st.title("Real-time Speech-to-Text")
    status_indicator = st.empty()
    text_output = st.empty()
    app_sst(status_indicator,text_output)

if __name__ == "__main__":
    main()
