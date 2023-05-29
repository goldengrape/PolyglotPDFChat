from langchain.chat_models import ChatOpenAI
from .StreamHandler import StreamDisplayHandler, StreamSpeakHandler
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

class TranslationService:
    def __init__(self, 
                stream_box,
                speak_box,
                model = "gpt-3.5-turbo" ,
                temperature = 0.3,
                voice={"synthesis":"zh-CN-XiaoxiaoNeural","rate":"+50.00%"},
                stream = True,
                speak = False,
                display_method='markdown',
                run_place="local",
                language="Chinese",
                ) -> None:
        self.voice=voice
        self.language = language
        stream_display_handler = StreamDisplayHandler(
            stream_box, display_method=display_method)
        stream_speak_handler = StreamSpeakHandler(
            container=speak_box,
            run_place=run_place,
            synthesis=self.voice["synthesis"],
            rate=self.voice.get("rate",""))
        if speak:
            callbacks=[stream_display_handler,stream_speak_handler]
        else:
            callbacks=[stream_display_handler]

        self.llm = ChatOpenAI(
                    model=model,
                    temperature=temperature,
                    streaming=stream,
                    callbacks=callbacks,
                )

    def translate(self, text, language="Chinese"):
        messages = [
            SystemMessage(content=f"You are a helpful assistant that translates the user message to {language}."),
            HumanMessage(content=text)
        ]
        result=self.llm(messages)
        return result.content 
