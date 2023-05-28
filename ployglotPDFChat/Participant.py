from .ChatRoom import ChatRoom
from .Message import Message
class Participant:
    # 这个类代表聊天室中的一个参与者，可以是主讲人或听众。每个参与者都有一个昵称和角色（主讲人或听众），以及他们所使用的语言和语音的偏好。参与者可以发送消息到聊天室，也可以播放语音。
    def __init__(self, nickname, role, language, voice, speed):
        if role not in ["speaker", "listener"]:
            raise ValueError("Role must be either 'speaker' or 'listener'.")
        self.nickname = nickname
        self.role = role
        self.language = language
        self.voice = voice
        self.speed = speed

    def send_message(self, room, text):
        if not isinstance(room, ChatRoom):
            raise TypeError("Room must be an instance of ChatRoom.")
        is_speaker = self.role == "speaker"
        message = Message(self.nickname, text, self.language)
        room.add_message(message, is_speaker)
