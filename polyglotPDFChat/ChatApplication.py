from .ChatRoom import ChatRoom

class ChatApplication:
    # 这个类代表聊天应用。这个应用维护了一个聊天室列表，可以创建新的聊天室，删除聊天室，显示所有的聊天室，以及向聊天室发送消息。
    def __init__(self):
        self.rooms = dict()  # Store all chat rooms in a dictionary with room names as keys.

    def create_room(self, room_name, speaker_name):
        # Check if the room already exists.
        if room_name in self.rooms:
            raise ValueError("A room with this name already exists.")
        # Create a new chat room and add it to the dictionary.
        self.rooms[room_name] = ChatRoom(room_name, speaker_name)
    
    def delete_room(self, room_name):
        # Check if the room exists.
        if room_name not in self.rooms:
            raise ValueError("No room with this name exists.")
        # Delete the room from the dictionary.
        del self.rooms[room_name]
    
    def display_rooms(self):
        # Print all room names.
        for room_name in self.rooms:
            print(room_name)
    
    def get_room(self, room_name):
        # Return the chat room with the given name.
        # If the room does not exist, raise an error.
        if room_name not in self.rooms:
            raise ValueError("No room with this name exists.")
        return self.rooms[room_name]
    
    def add_listener_to_room(self, room_name, listener_name):
        # Get the room and add the listener.
        room = self.get_room(room_name)
        room.add_listener(listener_name)
    
    def remove_listener_from_room(self, room_name, listener_name):
        # Get the room and remove the listener.
        room = self.get_room(room_name)
        room.remove_listener(listener_name)
    
    def send_message_to_room(self, room_name, sender_name, text):
        # Get the room and send the message.
        room = self.get_room(room_name)
        room.send_message(sender_name, text)
