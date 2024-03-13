from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from langchain_community.vectorstores import FAISS

from langchain_mongodb import MongoDBChatMessageHistory

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from os import environ


class AIClient:
    def __init__(self):
        pass


    def _load_embedding(self, vectorstore_path: str):
        embedder = OpenAIEmbeddings()
        return FAISS.load_local(vectorstore_path, embedder, allow_dangerous_deserialization=True)

    def _get_history(self, chat_id: str):
        mongo_url = environ.get('MONGO_URL', 'mongodb://localhost:27017/')
        return MongoDBChatMessageHistory(session_id=chat_id, connection_string=mongo_url)

    def _get_memory(self, chat_id: str):
        history = self._get_history(chat_id)
        return ConversationBufferMemory(chat_memory=history, return_messages=True, memory_key='chat_history')

    def create_embedding(self, chunks: list[str]):
        embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
        vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
        return vectorstore

    def quote_similarity(self, vectorstore_path: str, quote: str):
        call_name = "[AIClient][quote_similarity]"
        print(f"{call_name} - Getting quote similarity {vectorstore_path}")
        vectorstore = self._load_embedding(vectorstore_path)
        print(f"{call_name} - Invoking vectorstore")
        return vectorstore.as_retriever().invoke(quote)

    def get_chat_messages(self, chat_id: str):
        call_name = "[AIClient][get_chat_messages]"
        print(f"{call_name} - Getting chat messages for chat: {chat_id}")
        chat_message_history = self._get_history(chat_id)
        return chat_message_history.messages

    def send_new_message(self, chat_id: str, message: str, vectorstore_path: str):
        call_name = "[AIClient][send_new_message]"
        print(f"{call_name} - Sending new message to chat: {chat_id}")
        vectorstore = self._load_embedding(vectorstore_path)
        memory = self._get_memory(chat_id)
        print(f"{call_name} - memory loaded")
        llm = ChatOpenAI()
        conversational_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            memory=memory,
            retriever=vectorstore.as_retriever(),
        )

        new_message = conversational_chain({ 'question': message })
        print(f"{call_name} - New message: {new_message}")
        return new_message

