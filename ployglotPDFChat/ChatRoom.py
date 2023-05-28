from .Participant import Participant
from .Message import Message
from .TTS_service import TTS_service
from .translation_service import translation_service
class ChatRoom:
    # 这个类代表一个聊天室。每个聊天室都有一个名字，一个主讲人，一群听众，以及他们发送的消息。聊天室可以添加和删除听众，发送消息，显示所有的消息，以及导出所有的消息。当主讲人结束聊天时，他可以选择关闭并删除聊天室。
    def __init__(self, name, speaker):
        if not isinstance(speaker, Participant) or speaker.role != "speaker":
            raise ValueError("Speaker must be a Participant instance with role 'speaker'.")
        self.name = name
        self.speaker = speaker
        self.listeners = []
        self.speaker_messages = []
        self.listener_messages = []
        self.pdf_files = []

    def add_listener(self, listener):
        if not isinstance(listener, Participant) or listener.role != "listener":
            raise ValueError("Listener must be a Participant instance with role 'listener'.")
        if listener not in self.listeners:
            self.listeners.append(listener)

    def remove_listener(self, listener):
        if listener in self.listeners:
            self.listeners.remove(listener)

    def add_message(self, message, is_speaker):
        if not isinstance(message, Message):
            raise TypeError("Message must be an instance of Message.")
        if is_speaker:
            self.speaker_messages.append(message)
        else:
            self.listener_messages.append(message)

    def export_messages(self, is_speaker):
        messages = self.speaker_messages if is_speaker else self.listener_messages
        return "\n".join([message.text for message in messages])

    def add_pdf(self, pdf_file):
        # Here we assume pdf_file is a valid file path, in reality you may want to check if the file exists
        self.pdf_files.append(pdf_file)

    def broadcast_message(self, message):
        # Use the TTS service to convert the message text to speech.
        # This is a placeholder and should be replaced with actual TTS code.
        speech = TTS_service.convert(message.text)
        
        # Play the speech for speakers.
        for participant in self.speakers:
            participant.play_speech(speech, message.language)

    def translate_message(self, message, to_language):
        # Use the translation service to translate the message text.
        # This is a placeholder and should be replaced with actual translation code.
        translated_text = translation_service.translate(message.text, to_language)
        
        # Create a new message with the translated text.
        translated_message = Message(message.sender, translated_text, to_language)
        
        return translated_message