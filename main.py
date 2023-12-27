from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db import models
from db.database import engine
from routes import router_websocket, router_users, router_schools
import uvicorn

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")
app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    http_protocol = request.headers.get("x-forwarded-proto", "http")
    ws_protocol = "wss" if http_protocol == "https" else "ws"
    server_urn = request.url.netloc
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "http_protocol": http_protocol,
            "ws_protocol": ws_protocol,
            "server_urn": server_urn
        }
    )

app.include_router(router_websocket)
app.include_router(router_users)
app.include_router(router_schools)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
