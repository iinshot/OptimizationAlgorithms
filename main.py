from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn
from api.router_meta import router as meta_router
from api.router_optimize import router as optimize_router
import domain.algorithms
import domain.functions
from domain.autoload import autoload

autoload(domain.algorithms)
autoload(domain.functions)
app = FastAPI(title="Optimization Lab")
app.mount("/static", StaticFiles(directory="presentation/static"), name="static")
templates = Jinja2Templates(directory="presentation")
app.include_router(meta_router)
app.include_router(optimize_router)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )