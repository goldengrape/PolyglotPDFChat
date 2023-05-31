# `TranslationService` 类的主要方法概述如下：

# - `__init__(self, stream_box, speak_box, model, temperature, voice, stream, speak, display_method, run_place, language)`: 初始化翻译服务实例。其中，`stream_box` 和 `speak_box` 是用于显示和发音翻译结果的窗口；`model` 是选择的 OpenAI 模型；`temperature` 控制模型生成的随机性；`voice` 包含语音合成的相关信息；`stream` 和 `speak` 决定是否流式显示和发音翻译结果；`display_method` 指定显示方式；`run_place` 决定运行位置；`language` 是目标语言。

# - `translate(self, text, language)`: 将 `text` 翻译成指定的 `language`。

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
        content=f"You need tor translates the user message to {language}. the user message is inside tag <user_message>:\n\n<user_message>{text}<user_message>"
        messages = [
            SystemMessage(content=f"You are a helpful assistant that translates the user message to {language}."),
            HumanMessage(content=text)
        ]
        result=self.llm(messages)
        return result.content 
