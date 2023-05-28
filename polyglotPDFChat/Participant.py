from .Message import Message
from .TranslationService import TranslationService
class Participant:
    # 这个类代表聊天室中的一个参与者，可以是主讲人或听众。每个参与者都有一个昵称和角色（主讲人或听众），以及他们所使用的语言和语音的偏好。参与者可以发送消息到聊天室，也可以播放语音。
    def __init__(self, nickname, role, language, voice, speed,speak=True,run_place="local"):
        if role not in ["speaker", "listener"]:
            raise ValueError("Role must be either 'speaker' or 'listener'.")
        self.nickname = nickname
        self.role = role
        self.language = language
        self.voice = voice
        self.speed = speed
        self.translation_service = TranslationService(
            model="gpt-3.5-turbo",
            temperature=0.3,
            voice={"synthesis": voice, "rate": speed},
            stream=True,
            speak=speak,
            run_place=run_place,
            language=language,
        )

    def create_message(self, text):
        is_speaker = self.role == "speaker"
        return Message(self.nickname, text, self.language, is_speaker)
    
    def receive_message(self, message):
        # Translate the message text to the participant's language
        translated_text = self.translation_service.translate(message.text)
        
        # Create a new message with the translated text.
        translated_message = Message(message.sender, translated_text, self.language)
        
        return translated_message