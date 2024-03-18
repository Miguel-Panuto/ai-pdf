# AIPDF

This is a API that consists in send PDF files, create the embedding of them and then you can search for the relative terms inside the PDF, or you 
can create a Chat and ask like a chat.

## Endpoints

You can access the swagger at: /docs, there will be all endpoints, with open api descriptions.

All /api routes, all [pdf routes](#pdf) and [chat routes](#chat) uses a token, inside the header x-auth-token, this is inside the table tokens on postgres.

### PDF

| Method | Endpoint        | Arguments                                  | Description                                     |
|:------:|:----------------|:-------------------------------------------|:------------------------------------------------|
| GET    | /api/pdf        | Query Param: label, optional               | This will retrieve all PDFs with their labels   |
| POST   | /api/pdf/upload | Multipart: file File(PDF); label, optional | Where upload the PDF and create the vectorstore |
| POST   | /api/pdf/relative_quotes/{pdf_id} | Param: pdf_id, body: { "quote": "str" } | Find Relative quotes About |

## Chat

| Method | Endpoint        | Arguments                                  | Description                                     |
|:------:|:----------------|:-------------------------------------------|:------------------------------------------------|
| GET    | /api/chat       | Query Param: label, optional; name, optional | This will retrieve all chats, can be filtered by pdf label or chat name   |
| POST   | /api/chat | json: { "name": "str", "pdf_id": "uuid" } | Create chat if some saved pdf |
| PUT    | /api/chat/{chat_id} | json: { "name": "str", "pdf_id": "uuid" }, all optional | Change Chat name, or used pdf, or change them both |
| GET    | /api/chat/{chat_id} | Param: chat_id | Retrieve name, pdf and messages inside the chat |
| POST   | /api/chat/{chat_id}/message | json: { "message": "str" } | Send a new message for the llm proccess |

## How to setup

`One important thing is, the python version cannot be 3.12, because the Dependency-Injector isn't compatible with it, so if you use 3.12, please
install the 3.11 and create a venv with the 3.11 .`

With that set, first thing it is to install the dependencies, that is used

```bash
pip install -r requirements.txt
```

And now you can run, the entrypoint it is the __main__.py file, sou can run:

```bash
python __main__.py

```

Or

```bash
python .
```

The uvicorn will be setup at runtime.

## Database

There is 2 main databases, a postgres for management and mongodb for the messages.

You must have to push the SQL inside the `tables.sql` into your postgres database.
