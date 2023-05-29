from .Participant import Participant

class ChatRoom:
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

    def add_message(self, participant, text):
        if not isinstance(participant, Participant):
            raise TypeError("Participant must be an instance of Participant.")
        message = participant.create_message(text)
        if participant.role == "speaker":
            self.speaker_messages.append(message)
        else:
            self.listener_messages.append(message)

    def export_messages(self, is_speaker):
        messages = self.speaker_messages if is_speaker else self.listener_messages
        return "\n".join([message.text for message in messages])

    def add_pdf(self, pdf_file):
        # Here we assume pdf_file is a valid file path, in reality you may want to check if the file exists
        self.pdf_files.append(pdf_file)
