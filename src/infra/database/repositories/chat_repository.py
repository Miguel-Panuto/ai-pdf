from src.infra.database.database_engine import DatabaseEngine
from src.types.chat import Chat, ChatFinded


class ChatRepository:
    def __init__(self, database_engine: DatabaseEngine):
        self.db = database_engine

    def create(self, chat: Chat):
        result = self.db.sql_one('''
            INSERT INTO aipdf.chat (user_id, pdf_id, name, uuid)
            VALUES (%s, %s, %s, %s)
            RETURNING name, uuid
        ''', chat.user_id, chat.pdf_id, chat.name, chat.uuid)
        return {
            'name': result[0],
            'uuid': result[1]
        }

    def list_chats(self, user_id: int, name: str | None = None, pdf_label: str | None = None):
        result = self.db.sql_all(f"""
            SELECT chat.name, chat.uuid, pdf_vector.label, pdf_vector.uuid
            FROM aipdf.chat
            JOIN aipdf.pdf_vector ON aipdf.chat.pdf_id = aipdf.pdf_vector.id
            WHERE 
                chat.user_id = {user_id} AND 
                chat.name LIKE '%%{name if name else ''}%%' AND 
                pdf_vector.label LIKE  '%%{pdf_label if pdf_label else ''}%%'
        """)
        return [{ 'name': chat[0], 'uuid': chat[1], 'pdf': { 'label': chat[2], 'uuid': chat[3] } } for chat in result]

    def find_by_uuid(self, user_id: int, chat_uuid: str) -> ChatFinded:
        result = self.db.sql_one(f"""
            SELECT chat.name, chat.uuid, pdf_vector.label, pdf_vector.uuid, chat.id
            FROM aipdf.chat
            JOIN aipdf.pdf_vector ON aipdf.chat.pdf_id = aipdf.pdf_vector.id
            WHERE chat.user_id = {user_id} AND chat.uuid = '{chat_uuid}'
        """)
        return ChatFinded(
            name=result[0],
            uuid= result[1],
            chat_id=result[4],
            pdf= { 'label': result[2], 'uuid': result[3] }
        )

    def find_vectorstore_and_id(self, user_id: int, chat_uuid: str):
        result = self.db.sql_one(f"""
            SELECT pdf_vector.vectorstore_path, chat.id
            FROM aipdf.chat
            JOIN aipdf.pdf_vector ON aipdf.chat.pdf_id = aipdf.pdf_vector.id
            WHERE chat.user_id = {user_id} AND chat.uuid = '{chat_uuid}'
        """)
        return {
            'vectorstore': result[0],
            'id': result[1]
        }

    def update(self, user_id: int, chat_uuid: str, stmt: str):
        (id,) = self.db.sql_one(f"""
            UPDATE aipdf.chat
            {stmt}
            WHERE user_id = {user_id} AND uuid = '{chat_uuid}'
            RETURNING id
        """)
        result = self.db.sql_one(f'''
            SELECT chat.name, chat.uuid, pdf_vector.label, pdf_vector.uuid
            FROM aipdf.chat
            JOIN aipdf.pdf_vector ON aipdf.chat.pdf_id = aipdf.pdf_vector.id
            WHERE chat.id = {id}
        ''')
        return {
            'name': result[0],
            'uuid': result[1],
            'pdf': { 'label': result[2], 'uuid': result[3] }
        }
