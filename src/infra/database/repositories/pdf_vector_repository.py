from src.infra.database.database_engine import DatabaseEngine
from src.types.pdf_vector import PdfVector


class PdfVectorRepository:
    def __init__(self, database_engine: DatabaseEngine):
        self.db = database_engine

    def create_relation(self, pdf: PdfVector):
        call_name = '[PdfVectorRepository][create_relation]'
        print(f'{call_name} - Creating pdf relation: {pdf}')
        vector_db = self.db.sql_one(f"""
            INSERT INTO aipdf.pdf_vector(user_id, vectorstore_path, label, uuid)
            VALUES ({pdf.user_id}, '{pdf.vectorstore_path}', '{pdf.label}', '{pdf.uuid}') 
            RETURNING label, uuid
        """)
        return {
            'label': vector_db[0],
            'uuid': vector_db[1]
        }


    def get_user_pdf(self, user_id: int, label: str | None = None):
        call_name = '[PdfVectorRepository][get_user_pdf]'
        print(f'{call_name} - Getting user pdfs for user and label: {user_id} - {label}')
        all_pdfs =  self.db.sql_all(f"""
            SELECT label, uuid
            FROM aipdf.pdf_vector
            WHERE user_id = {user_id} AND label LIKE '%%{label if label else ''}%%'
        """)
        return [{'label': pdf[0], 'uuid': pdf[1]} for pdf in all_pdfs]


    def get_pdf_vectorstore(self, uuid: str, user_id: int):
        call_name = '[PdfVectorRepository][get_pdf]'
        print(f'{call_name} - Getting pdf for uuid: {uuid}')
        pdf = self.db.sql_one('''
            SELECT vectorstore_path
            FROM aipdf.pdf_vector
            WHERE uuid = %s AND user_id = %s
        ''', uuid, user_id)
        return pdf[0]


    def get_id_by_uuid(self, uuid: str, user_id: int) -> int:
        call_name = '[PdfVectorRepository][get_id_by_uuid]'
        print(f'{call_name} - Getting id by uuid: {uuid}')
        pdf = self.db.sql_one('''
            SELECT id
            FROM aipdf.pdf_vector
            WHERE uuid = %s AND user_id = %s
        ''', uuid, user_id)
        return pdf[0]
