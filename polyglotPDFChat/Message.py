# 这是 `Message` 类的方法概述：

# - `__init__(self, sender, text, language)`: 构造方法。它需要三个参数：`sender`（消息的发送者，必须是一个 `Participant` 实例），`text`（消息的文本），以及 `language`（消息的语言）。

# - `display(self)`: 此方法用于显示消息。它将返回一个字符串，该字符串包含了消息的发送时间、发送者的名字，以及消息的文本。

from datetime import datetime

class Message:
    def __init__(self, sender, text, language):
        self.sender = sender
        self.text = text
        self.language = language
        self.timestamp = datetime.now()

    def display(self):
        time = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"{time} - {self.sender.name}: {self.text}"

