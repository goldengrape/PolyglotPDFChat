from datetime import datetime

class Message:
    # 这个类代表聊天室中的一条消息。每条消息都有一个发送者（参与者），消息文本，发送时间，以及消息的语言。可以通过 display() 方法来显示消息。该方法也负责将消息文本翻译成参与者所使用的语言，并通过 TTS_service 转化为语音。
    def __init__(self, sender, text, language):
        self.sender = sender
        self.text = text
        self.language = language
        self.timestamp = datetime.now()

    def display(self):
        time = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"{time} - {self.sender.name}: {self.text}"

