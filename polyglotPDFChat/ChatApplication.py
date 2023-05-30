# `ChatApplication` 是一个聊天应用类，它维护了一个聊天室列表，并可以进行一些操作，例如创建新的聊天室，删除聊天室，显示所有的聊天室，向聊天室发送消息等。以下是其方法的详细描述：

# - `__init__`: 这是类的初始化方法。它没有参数，但会初始化一个字典 `self.rooms`，该字典用于存储所有的聊天室，其中键是聊天室的名称。

# - `create_room(room_name, speaker)`: 此方法用于创建一个新的聊天室并将其添加到 `self.rooms` 字典中。它需要两个参数：`room_name`（聊天室的名称）和 `speaker`（演讲者）。

# - `delete_room(room_name)`: 此方法用于从 `self.rooms` 字典中删除一个聊天室。它需要一个参数：`room_name`（要删除的聊天室的名称）。

# - `display_rooms()`: 此方法用于打印出所有聊天室的名称。它没有参数。

# - `get_room(room_name)`: 此方法用于返回一个具有给定名称的聊天室。如果该聊天室不存在，则会抛出错误。它需要一个参数：`room_name`（要返回的聊天室的名称）。

# add_listener_to_room(room_name, listener_name): 此方法用于向聊天室添加听众。它需要两个参数：room_name（聊天室的名称）和 listener_name（要添加的听众的名称）。

# remove_listener_from_room(room_name, listener_name): 此方法用于从聊天室中移除听众。它需要两个参数：room_name（聊天室的名称）和 listener_name（要移除的听众的名称）。

# - `send_message_to_room(room_name, sender_name, text)`: 此方法用于向聊天室发送消息。它需要三个参数：`room_name`（聊天室的名称），`sender_name`（发送者的名称）和 `text`（要发送的消息文本）。

from .ChatRoom import ChatRoom

class ChatApplication:
    def __init__(self):
        self.rooms = dict()  # Store all chat rooms in a dictionary with room names as keys.

    def create_room(self, room_name, speaker):
        # Check if the room already exists.
        if room_name in self.rooms:
            # raise ValueError("A room with this name already exists.")
            pass
        else:
            # check the type of speaker
            print("speaker type: ",type(speaker))
            # Create a new chat room and add it to the dictionary.
            self.rooms[room_name] = ChatRoom(room_name, speaker)
    
    def delete_room(self, room_name):
        # Check if the room exists.
        if room_name not in self.rooms:
            raise ValueError("No room with this name exists.")
        # Delete the room from the dictionary.
        del self.rooms[room_name]
    
    # def display_rooms(self):
    #     # Print all room names.
    #     for room_name in self.rooms:
    #         print(room_name)
    def display_rooms(self):
        if len(self.rooms) > 0:
            return list(self.rooms.keys())
        else:
            return []

    
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
