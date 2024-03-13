from fastapi import FastAPI 
from fastapi.responses import JSONResponse

import uvicorn

from src.interfaces.http.pdf_router import router as pdf_router
from src.interfaces.http.chat_router import router as chat_router
from src.auth import find_user_by_token 

from os import environ

app = FastAPI()

@app.middleware("http")
async def validate(request, call_next):
    path = request.url.path
    if '/api' not in path:
        return await call_next(request)
    try:
        user_id = find_user_by_token.execute(request.headers['x-auth-token'])
        if user_id: 
            request.state.user_id = user_id
            return await call_next(request)
        raise Exception('Unauthorized')
    except Exception as e:
        return JSONResponse(status_code=403, content={"error": str(e)})

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(pdf_router)
app.include_router(chat_router)

def start_server():
    port = environ.get('PORT', '3000')
    port = int(port)
    config = uvicorn.Config("src.interfaces.http.server:app", host='0.0.0.0', port=port, log_level="info")
    server = uvicorn.Server(config)
    server.run()
