from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    
    # JSON serializable한 에러로 변환
    serializable_errors = []
    for error in exc.errors():
        serializable_error = {
            "type": error.get("type"),
            "loc": error.get("loc"),
            "msg": error.get("msg"),
            "input": error.get("input")
        }
        # ValueError context 처리
        if "ctx" in error and "error" in error["ctx"]:
            error_obj = error["ctx"]["error"]
            if isinstance(error_obj, ValueError):
                serializable_error["ctx"] = {"error": str(error_obj)}
            else:
                serializable_error["ctx"] = error["ctx"]
        serializable_errors.append(serializable_error)
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": "입력 데이터가 올바르지 않습니다",
            "errors": serializable_errors
        }
    )

async def integrity_error_handler(request: Request, exc: IntegrityError):
    logger.error(f"Database integrity error: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={
            "detail": "데이터베이스 제약 조건 위반",
            "message": "중복된 데이터가 존재하거나 필수 필드가 누락되었습니다"
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "서버 내부 오류가 발생했습니다",
            "message": "잠시 후 다시 시도해주세요"
        }
    )