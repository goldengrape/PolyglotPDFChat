import streamlit as st
import numpy as np
from streamlit_webrtc import WebRtcMode, webrtc_streamer
# from streamlit_webrtc import VideoTransformerBase, VideoTransformerContext

from pydub import AudioSegment
import queue, pydub, tempfile, openai, os, time


def save_audio(audio_segment: AudioSegment, base_filename: str) -> None:
    """
    Save an audio segment to a .wav file.

    Args:
        audio_segment (AudioSegment): The audio segment to be saved.
        base_filename (str): The base filename to use for the saved .wav file.
    """
    filename = f"{base_filename}_{int(time.time())}.wav"
    audio_segment.export(filename, format="wav")

def transcribe(audio_segment: AudioSegment, debug: bool = False) -> str:
    """
    Transcribe an audio segment using OpenAI's Whisper ASR system.

    Args:
        audio_segment (AudioSegment): The audio segment to transcribe.
        debug (bool): If True, save the audio segment for debugging purposes.

    Returns:
        str: The transcribed text.
    """
    if debug:
        save_audio(audio_segment, "debug_audio")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        audio_segment.export(tmpfile.name, format="wav")
        answer = openai.Audio.transcribe(
            "whisper-1",
            tmpfile,
            temperature=0.2,
            prompt="",
        )["text"]
        tmpfile.close()  
        os.remove(tmpfile.name)
        return answer

def frame_energy(frame):
    """
    Compute the energy of an audio frame.

    Args:
        frame (VideoTransformerBase.Frame): The audio frame to compute the energy of.

    Returns:
        float: The energy of the frame.
    """
    samples = np.frombuffer(frame.to_ndarray().tobytes(), dtype=np.int16)
    return np.sqrt(np.mean(samples**2))
 
def process_audio_frames(audio_frames, sound_chunk, silence_frames, energy_threshold):
    """
    Process a list of audio frames.

    Args:
        audio_frames (list[VideoTransformerBase.Frame]): The list of audio frames to process.
        sound_chunk (AudioSegment): The current sound chunk.
        silence_frames (int): The current number of silence frames.
        energy_threshold (int): The energy threshold to use for silence detection.

    Returns:
        tuple[AudioSegment, int]: The updated sound chunk and number of silence frames.
    """
    for audio_frame in audio_frames:
        sound_chunk = add_frame_to_chunk(audio_frame, sound_chunk)

        energy = frame_energy(audio_frame)
        if energy < energy_threshold:
            silence_frames += 1
        else:
            silence_frames = 0

    return sound_chunk, silence_frames

def add_frame_to_chunk(audio_frame, sound_chunk):
    """
    Add an audio frame to a sound chunk.

    Args:
        audio_frame (VideoTransformerBase.Frame): The audio frame to add.
        sound_chunk (AudioSegment): The current sound chunk.

    Returns:
        AudioSegment: The updated sound chunk.
    """
    sound = pydub.AudioSegment(
        data=audio_frame.to_ndarray().tobytes(),
        sample_width=audio_frame.format.bytes,
        frame_rate=audio_frame.sample_rate,
        channels=len(audio_frame.layout.channels),
    )
    sound_chunk += sound
    return sound_chunk

def handle_silence(sound_chunk, silence_frames, silence_frames_threshold, text_output):
    """
    Handle silence in the audio stream.

    Args:
        sound_chunk (AudioSegment): The current sound chunk.
        silence_frames (int): The current number of silence frames.
        silence_frames_threshold (int): The silence frames threshold.
        text_output (st.empty): The Streamlit text output object.

    Returns:
        tuple[AudioSegment, int]: The updated sound chunk and number of silence frames.
    """
    if silence_frames >= silence_frames_threshold:
        if len(sound_chunk) > 0:
            text = transcribe(sound_chunk)
            text_output.write(text)
            sound_chunk = pydub.AudioSegment.empty()
            silence_frames = 0

    return sound_chunk, silence_frames

def handle_queue_empty(sound_chunk, text_output):
    """
    Handle the case where the audio frame queue is empty.

    Args:
        sound_chunk (AudioSegment): The current sound chunk.
        text_output (st.empty): The Streamlit text output object.

    Returns:
        AudioSegment: The updated sound chunk.
    """
    if len(sound_chunk) > 0:
        text = transcribe(sound_chunk)
        text_output.write(text)
        sound_chunk = pydub.AudioSegment.empty()

    return sound_chunk

def app_sst(
        status_indicator,
        text_output,
        timeout=3, 
        energy_threshold=2000, 
        silence_frames_threshold=100
        ):
    """
    The main application function for real-time speech-to-text. 

    This function creates a WebRTC streamer, starts receiving audio data, processes the audio frames, 
    and transcribes the audio into text when there is silence longer than a certain threshold.

    Args:
        status_indicator: A Streamlit object for showing the status (running or stopping).
        text_output: A Streamlit object for showing the transcribed text.
        timeout (int, optional): Timeout for getting frames from the audio receiver. Default is 3 seconds.
        energy_threshold (int, optional): The energy threshold below which a frame is considered silence. Default is 2000.
        silence_frames_threshold (int, optional): The number of consecutive silence frames to trigger transcription. Default is 100 frames.
    """
    webrtc_ctx = webrtc_streamer(
        key="speech-to-text",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        media_stream_constraints={"video": False, "audio": True},
    )

    sound_chunk = pydub.AudioSegment.empty()
    silence_frames = 0

    while True:
        if webrtc_ctx.audio_receiver:
            status_indicator.write("Running. Say something!")

            try:
                audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=timeout)
            except queue.Empty:
                status_indicator.write("No frame arrived.")
                sound_chunk = handle_queue_empty(sound_chunk, text_output)
                continue

            sound_chunk, silence_frames = process_audio_frames(audio_frames, sound_chunk, silence_frames, energy_threshold)
            sound_chunk, silence_frames = handle_silence(sound_chunk, silence_frames, silence_frames_threshold, text_output)
        else:
            status_indicator.write("Stopping.")
            if len(sound_chunk) > 0:
                text = transcribe(sound_chunk.raw_data)
                text_output.write(text)
            break

def main():
    st.title("Real-time Speech-to-Text")
    status_indicator = st.empty()
    text_output = st.empty()
    app_sst(status_indicator,text_output)

if __name__ == "__main__":
    main()

