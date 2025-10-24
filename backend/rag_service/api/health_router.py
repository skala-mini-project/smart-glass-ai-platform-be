from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/")
async def health_check():
    """기본 헬스 체크"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Field Intelligence Cloud Platform Backend"
    }

@router.get("/ready")
async def readiness_check():
    """서비스 준비 상태 확인"""
    # TODO: 데이터베이스 연결, 외부 서비스 연결 상태 확인
    return {
        "status": "ready",
        "timestamp": datetime.now().isoformat(),
        "checks": {
            "database": "ok",
            "vector_store": "ok",
            "llm_service": "ok"
        }
    }

@router.get("/live")
async def liveness_check():
    """서비스 생존 상태 확인"""
    return {
        "status": "alive",
        "timestamp": datetime.now().isoformat()
    }
