# 这是 `ChatRoom` 类的方法概述：

# - `__init__(self, name, speaker)`: 构造方法。它需要两个参数：`name`（聊天室的名称）和 `speaker`（一个 `Participant` 实例，其角色必须是 "speaker"）。

# - `add_listener(self, listener)`: 此方法用于向聊天室添加听众。它需要一个参数：`listener`（一个 `Participant` 实例，其角色必须是 "listener"）。

# - `remove_listener(self, listener)`: 此方法用于从聊天室中移除听众。它需要一个参数：`listener`（一个 `Participant` 实例，其角色必须是 "listener"）。

# - `add_message(self, participant, text)`: 此方法用于向聊天室添加消息。它需要两个参数：`participant`（一个 `Participant` 实例）和 `text`（要添加的消息文本）。

# - `export_messages(self, is_speaker)`: 此方法用于导出聊天室的消息。它需要一个参数：`is_speaker`（一个布尔值，如果为 `True`，则导出主讲人的消息，否则导出听众的消息）。

# - `add_pdf(self, pdf_file)`: 此方法用于向聊天室添加 PDF 文件。它需要一个参数：`pdf_file`（要添加的 PDF 文件的文件路径）。在实际应用中，您可能需要检查文件是否存在。

from .Participant import Participant

class ChatRoom:
    def __init__(self, name, speaker):
        if not isinstance(speaker, Participant):
            print("not a participant",speaker)
            # raise TypeError("Speaker must be an instance of Participant.")
        if speaker.role != "speaker":
            print("not a speaker",speaker)
            print(type(speaker))
            # raise ValueError("Speaker must be a Participant instance with role 'speaker'.")
        self.name = name
        self.speaker = speaker
        self.listeners = set()
        self.speaker_messages = []
        self.listener_messages = []
        self.all_messages = []
        self.pdf_files = []

    def add_listener(self, listener):
        if not isinstance(listener, Participant) :
            print("not a participant",listener)
        #     raise TypeError("Speaker must be an instance of Participant.")
        if listener.role != "listener":
            print("not a listener",listener)
        #     raise ValueError("Listener must be a Participant instance with role 'listener'.")
        if listener not in self.listeners:
            self.listeners.add(listener)

    def remove_listener(self, listener):
        if listener in self.listeners:
            self.listeners.remove(listener)

    def add_message(self, participant, text):
        # if not isinstance(participant, Participant):
        #     raise TypeError("Participant must be an instance of Participant.")
        message = participant.create_message(text)
        if participant.role == "speaker":
            self.speaker_messages.append(message)
        else:
            self.listener_messages.append(message)
        self.all_messages.append(message)

    def export_messages(self, display_role=["speaker","listener"]):
        if len(display_role)==1:
            if display_role[0]=="speaker":
                messages=self.speaker_messages
            elif display_role[0]=="listener":
                messages=self.listener_messages
        elif len(display_role)==2:
            messages=self.all_messages
        else:
            messages=self.all_messages
        return "\n\n".join([message.display() for message in messages])
        # return messages
    
    def speaker_last_message(self):
        if len(self.speaker_messages)>=1:
            last_message=self.speaker_messages[-1]
        else:
            last_message=""
        return last_message

    def add_pdf(self, pdf_file):
        # Here we assume pdf_file is a valid file path, in reality you may want to check if the file exists
        self.pdf_files.append(pdf_file)
