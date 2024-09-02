from langchain_openai import ChatOpenAI


class ChatModelSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ChatModelSingleton, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self, model="gpt-4o-mini"):
        self.model = ChatOpenAI(model=model)

    def get_model(self):
        return self.model