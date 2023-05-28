from langchain.callbacks.base import BaseCallbackHandler
import azure.cognitiveservices.speech as speechsdk
import os
import base64
import time
class StreamDisplayHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text="", display_method='markdown'):
        self.container = container
        self.text = initial_text
        self.display_method = display_method
        self.new_sentence = ""

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.new_sentence += token

        display_function = getattr(self.container, self.display_method, None)
        if display_function is not None:
            display_function(self.text)
        else:
            raise ValueError(f"Invalid display_method: {self.display_method}")

    def on_llm_end(self, response, **kwargs) -> None:
        self.text=""


class StreamSpeakHandler(BaseCallbackHandler):
    def __init__(self, 
        container,
        run_place="cloud",
        synthesis="zh-CN-XiaoxiaoNeural", 
        rate="+50.00%"):
        self.container = container
        self.run_place=run_place
        self.new_sentence = ""
        # Initialize the speech synthesizer
        self.synthesis=synthesis
        self.rate=rate
        self.speech_synthesizer = self.settings(synthesis)

    def settings(self, synthesis):
        speech_config = speechsdk.SpeechConfig(
            subscription=os.environ.get('SPEECH_KEY'), 
            region=os.environ.get('SPEECH_REGION')
        )
        audio_output_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        
        speech_config.speech_synthesis_voice_name=synthesis

        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output_config)
        return speech_synthesizer

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.new_sentence += token
        # Check if the new token forms a sentence.
        if token in ".:!?。：！？\n":
            # Synthesize the new sentence
            speak_this = self.new_sentence

            ssml_text=f"""<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" version="1.0" xml:lang="en-US">
    <voice name="{self.synthesis}">
    <prosody rate="{self.rate}">
            {speak_this}
    </prosody>
    </voice>
</speak>"""


            if self.run_place !="local":
                self.speak_streamlit_cloud(ssml_text)
            else:
                self.speak_ssml_async(ssml_text)
            self.new_sentence = ""

    def on_llm_end(self, response, **kwargs) -> None:
        self.new_sentence = ""

    def speak_ssml_async(self, text):
        speech_synthesis_result = self.speech_synthesizer.speak_ssml_async(text).get()
        if speech_synthesis_result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f'Error synthesizing speech: {speech_synthesis_result.reason}')
    def speak_streamlit_cloud(self,text):
        speech_synthesis_result = self.speech_synthesizer.speak_ssml_async(text).get()
        if speech_synthesis_result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f'Error synthesizing speech: {speech_synthesis_result.reason}')
        else:
            audio_stream = speech_synthesis_result.audio_data
            audio_base64 = base64.b64encode(audio_stream).decode('utf-8')
            audio_tag = f'<audio autoplay="true" src="data:audio/wav;base64,{audio_base64}">'
            self.container.markdown(audio_tag, unsafe_allow_html=True)
            number_of_seconds = speech_synthesis_result.audio_duration.seconds
            time.sleep(number_of_seconds)
            
