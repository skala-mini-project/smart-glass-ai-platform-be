# Vision AI API Router
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import cv2
import numpy as np
import json
import io
from datetime import datetime
import logging

from vision_service.core.detector import VisionDetector

router = APIRouter()
logger = logging.getLogger(__name__)

# 전역 Vision Detector 인스턴스
vision_detector = VisionDetector()

# ===========================================
# Pydantic 모델 정의
# ===========================================

class DetectionRequest(BaseModel):
    """단일 이미지 탐지 요청"""
    image_data: Optional[str] = None  # base64 인코딩된 이미지
    confidence_threshold: float = 0.5
    max_objects: int = 10

class DetectionResponse(BaseModel):
    """탐지 결과 응답"""
    frame_id: int
    timestamp: str
    fps: float
    resolution: List[int]
    scene_context: str
    objects: List[Dict[str, Any]]
    processing_time_ms: float
    model_version: str
    status: str

class StreamConfig(BaseModel):
    """스트림 설정"""
    resolution: List[int] = [640, 480]
    fps: int = 30
    confidence_threshold: float = 0.5
    show_bbox: bool = True
    show_labels: bool = True

# ===========================================
# API 엔드포인트
# ===========================================

@router.get("/status")
async def get_vision_status():
    """Vision AI 서비스 상태 확인"""
    return {
        "status": "active",
        "service": "Vision AI Service",
        "version": "1.0.0",
        "model_loaded": vision_detector.model_loaded,
        "model_version": "yolov8n"
    }

@router.post("/detect/image", response_model=DetectionResponse)
async def detect_image(request: DetectionRequest):
    """단일 이미지 객체 탐지 (목업)"""
    try:
        logger.info("이미지 탐지 요청 받음")
        
        # 목업용 더미 이미지 생성
        dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(dummy_frame, "Mock Image", (200, 240), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        
        # 객체 탐지 실행
        result = vision_detector.detect_objects(dummy_frame)
        
        return DetectionResponse(**result)
        
    except Exception as e:
        logger.error(f"이미지 탐지 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/detect/upload")
async def detect_uploaded_image(file: UploadFile = File(...)):
    """업로드된 이미지 파일 탐지"""
    try:
        # 업로드된 파일 읽기
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            raise HTTPException(status_code=400, detail="유효하지 않은 이미지 파일")
        
        # 객체 탐지 실행
        result = vision_detector.detect_objects(frame)
        
        return result
        
    except Exception as e:
        logger.error(f"업로드 이미지 탐지 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stream/start")
async def start_stream(config: StreamConfig = StreamConfig()):
    """실시간 스트림 시작 (목업)"""
    try:
        logger.info(f"스트림 시작: {config.resolution} @ {config.fps}fps")
        
        return {
            "status": "started",
            "stream_id": f"stream_{int(datetime.now().timestamp())}",
            "config": config.dict(),
            "message": "실시간 스트림이 시작되었습니다 (목업 모드)"
        }
        
    except Exception as e:
        logger.error(f"스트림 시작 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stream/frame")
async def get_current_frame():
    """현재 프레임 정보 조회 (목업)"""
    try:
        # 목업용 더미 프레임 생성
        dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(dummy_frame, f"Mock Frame {int(datetime.now().timestamp())}", 
                   (150, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # 객체 탐지 실행
        result = vision_detector.detect_objects(dummy_frame)
        
        return result
        
    except Exception as e:
        logger.error(f"프레임 조회 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stream/stop")
async def stop_stream():
    """실시간 스트림 종료"""
    try:
        logger.info("스트림 종료 요청")
        
        return {
            "status": "stopped",
            "message": "실시간 스트림이 종료되었습니다"
        }
        
    except Exception as e:
        logger.error(f"스트림 종료 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/objects/history")
async def get_object_history(limit: int = 10):
    """객체 탐지 히스토리 조회 (목업)"""
    try:
        # 목업용 히스토리 데이터
        history = []
        for i in range(min(limit, 5)):
            history.append({
                "frame_id": int(datetime.now().timestamp() * 1000) - i * 1000,
                "timestamp": datetime.now().isoformat(),
                "objects_count": i + 1,
                "detected_objects": ["person", "laptop", "cup"][:i+1]
            })
        
        return {
            "status": "success",
            "history": history,
            "total_count": len(history)
        }
        
    except Exception as e:
        logger.error(f"히스토리 조회 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
