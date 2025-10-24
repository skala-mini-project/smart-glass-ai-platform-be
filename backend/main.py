from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rag_service.api.rag_router import router as rag_router
from rag_service.api.health_router import router as health_router
from vision_service.api.vision_router import router as vision_router

app = FastAPI(
    title="Field Intelligence Cloud Platform - Backend",
    description="Smart Glass AI Platform Backend API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발용, 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(rag_router, prefix="/rag", tags=["rag"])
app.include_router(vision_router, prefix="/vision", tags=["vision"])

@app.get("/")
async def root():
    return {"message": "Field Intelligence Cloud Platform Backend API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
