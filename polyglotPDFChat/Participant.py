# 这是 `Participant` 类的方法概述：

# - `__init__(self, name, role, language, voice, speed, stream_box, speak_box, speak=True, run_place="local")`: 构造方法。它需要以下参数：

#   - `name`: 参与者的名字。
#   - `role`: 参与者的角色，可以是 "speaker" 或 "listener"。
#   - `language`: 参与者的语言。
#   - `voice`: 参与者的语音设置。
#   - `speed`: 语音的速度。
#   - `stream_box`: 用于接收实时翻译结果的窗口。
#   - `speak_box`: 用于接收朗读结果的窗口。
#   - `speak`: 一个布尔值，表示是否需要朗读翻译结果。
#   - `run_place`: 表示运行翻译服务的地点，可以是 "local" 或 "cloud"。

# - `create_message(self, text)`: 这个方法用于创建一个新的 `Message` 实例。它需要一个参数：`text`（消息的文本）。

# - `receive_message(self, message)`: 这个方法用于接收一个 `Message` 实例。首先，它会把消息的文本翻译成参与者的语言，然后用翻译后的文本创建一个新的 `Message` 实例，并返回这个实例。
from typing import Any
from .Message import Message
from .TranslationService import TranslationService
class Participant:
    def __init__(self, name, role, language, voice, speed,
                stream_box,
                speak_box,
                speak=True,
                openai_key="",
                speech_key="",
                speech_region="westus",
                run_place="cloud"):
        if role not in ["speaker", "listener"]:
            raise ValueError("Role must be either 'speaker' or 'listener'.")
        self.name = name
        self.role = role
        self.language = language
        self.voice = voice
        self.speed = speed
        self.translation_service = TranslationService(
            openai_key=openai_key,
            speech_key=speech_key,
            speech_region=speech_region,
            stream_box=stream_box,
            speak_box=speak_box,
            model="gpt-3.5-turbo",
            temperature=0.3,
            voice={"synthesis": voice, "rate": speed},
            stream=True,
            speak=speak,
            run_place=run_place,
            language=language,
        )

    def create_message(self, text):
        return Message(self.name, text, self.language)
    
    def receive_message(self, message):
        # Translate the message text to the participant's language
        # 先判断是否收到的是message实例
        if not isinstance(message, Message):
            return message
        if message.language == self.language:
            translated_text = message.text
        else:
            translated_text = self.translation_service.translate(message.text)
        
        # Create a new message with the translated text.
        translated_message = Message(message.sender, translated_text, self.language)
        
        return translated_message
    
    def __repr__(self):
        return f"""{self.name} as {self.role} in {self.language}"""