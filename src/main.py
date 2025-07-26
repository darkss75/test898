from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.exc import IntegrityError
from .database import database
from .models import member
from .routers import member_router
from .utils.exceptions import (
    validation_exception_handler,
    integrity_error_handler,
    general_exception_handler
)

member.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="회원 관리 시스템",
    description="FastAPI를 사용한 회원 관리 API",
    version="1.0.0"
)

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 정적 파일 설정 (디렉토리가 존재할 때만)
import os
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(Exception, general_exception_handler)

# 메인 페이지 라우트 (출입 확인)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 관리자 페이지 라우트
@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

app.include_router(member_router.router, prefix="/api/v1", tags=["members"])