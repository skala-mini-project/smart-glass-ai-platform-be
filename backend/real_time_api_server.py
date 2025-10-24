# 실시간 웹캠 스트림 API 구현
import cv2
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse, JSONResponse
import asyncio
import json
from datetime import datetime
import base64
import io
from PIL import Image
import threading
import queue

# 백엔드 모듈 import
import sys
import os
sys.path.append(os.path.dirname(__file__))

from vision_service.core.detector import VisionDetector
from rag_service.services.rag_service import RAGService
from vision_service.services.ocr_service import OCRService

class WebcamStreamManager:
    """웹캠 스트림 관리자"""
    
    def __init__(self):
        self.vision_detector = VisionDetector()
        self.rag_service = RAGService()
        self.ocr_service = OCRService()
        self.cap = None
        self.is_streaming = False
        self.frame_queue = queue.Queue(maxsize=10)
        self.detection_history = []
        self.frame_count = 0
    
    def start_stream(self):
        """스트림 시작"""
        if self.is_streaming:
            return {"status": "already_streaming"}
        
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                return {"status": "error", "message": "웹캠을 열 수 없습니다"}
            
            # 웹캠 설정
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            self.is_streaming = True
            self.frame_count = 0
            
            # 스트림 스레드 시작
            self.stream_thread = threading.Thread(target=self._capture_frames)
            self.stream_thread.daemon = True
            self.stream_thread.start()
            
            return {"status": "success", "message": "스트림이 시작되었습니다"}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def stop_stream(self):
        """스트림 중지"""
        self.is_streaming = False
        if self.cap:
            self.cap.release()
        return {"status": "success", "message": "스트림이 중지되었습니다"}
    
    def _capture_frames(self):
        """프레임 캡처 스레드"""
        while self.is_streaming and self.cap:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            self.frame_count += 1
            
            # 객체 탐지
            detection_result = self.vision_detector.detect_objects(frame)
            
            # OCR 텍스트 추출
            ocr_result = self.ocr_service.extract_text(frame)
            
            # 결과 시각화
            processed_frame = self._visualize_results(frame, detection_result, ocr_result)
            
            # 히스토리 저장
            frame_info = {
                "frame_id": self.frame_count,
                "timestamp": datetime.now().isoformat(),
                "detections": len(detection_result['objects']),
                "texts": len(ocr_result['texts']),
                "objects": detection_result['objects'],
                "texts": ocr_result['texts']
            }
            self.detection_history.append(frame_info)
            
            # 큐에 프레임 추가 (오래된 프레임 제거)
            if self.frame_queue.full():
                try:
                    self.frame_queue.get_nowait()
                except queue.Empty:
                    pass
            
            self.frame_queue.put({
                "frame": processed_frame,
                "detection_result": detection_result,
                "ocr_result": ocr_result,
                "frame_info": frame_info
            })
    
    def _visualize_results(self, frame, detection_result, ocr_result):
        """결과 시각화"""
        processed_frame = frame.copy()
        
        # 객체 탐지 결과 그리기
        for obj in detection_result['objects']:
            bbox = obj['bbox']
            x, y, w, h = bbox['x'], bbox['y'], bbox['width'], bbox['height']
            
            # 바운딩 박스 그리기
            cv2.rectangle(processed_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # 라벨과 신뢰도 표시
            label = f"{obj['label']}: {obj['confidence']:.2f}"
            cv2.putText(processed_frame, label, (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # OCR 텍스트 결과 그리기
        for text_info in ocr_result['texts']:
            bbox = text_info['bbox']
            x, y, w, h = bbox[0], bbox[1], bbox[2], bbox[3]
            
            # 텍스트 영역 그리기
            cv2.rectangle(processed_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
            # 텍스트 표시
            cv2.putText(processed_frame, text_info['text'], (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        # 프레임 정보 표시
        info_text = f"Frame: {self.frame_count} | Objects: {len(detection_result['objects'])} | Texts: {len(ocr_result['texts'])}"
        cv2.putText(processed_frame, info_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return processed_frame
    
    def get_latest_frame(self):
        """최신 프레임 가져오기"""
        try:
            return self.frame_queue.get_nowait()
        except queue.Empty:
            return None
    
    def get_stream_status(self):
        """스트림 상태 확인"""
        return {
            "is_streaming": self.is_streaming,
            "frame_count": self.frame_count,
            "queue_size": self.frame_queue.qsize(),
            "total_detections": sum(len(frame['objects']) for frame in self.detection_history),
            "total_texts": sum(len(frame['texts']) for frame in self.detection_history)
        }

# 전역 스트림 매니저
stream_manager = WebcamStreamManager()

# FastAPI 앱 생성
app = FastAPI(title="Real-time Vision AI API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Real-time Vision AI API Server"}

@app.post("/stream/start")
async def start_stream():
    """스트림 시작"""
    result = stream_manager.start_stream()
    return JSONResponse(content=result)

@app.post("/stream/stop")
async def stop_stream():
    """스트림 중지"""
    result = stream_manager.stop_stream()
    return JSONResponse(content=result)

@app.get("/stream/status")
async def get_stream_status():
    """스트림 상태 확인"""
    status = stream_manager.get_stream_status()
    return JSONResponse(content=status)

@app.get("/stream/frame")
async def get_latest_frame():
    """최신 프레임 가져오기 (JSON)"""
    frame_data = stream_manager.get_latest_frame()
    if frame_data is None:
        return JSONResponse(content={"status": "no_frame"})
    
    # OpenCV 이미지를 base64로 변환
    frame = frame_data["frame"]
    _, buffer = cv2.imencode('.jpg', frame)
    frame_base64 = base64.b64encode(buffer).decode('utf-8')
    
    return JSONResponse(content={
        "status": "success",
        "frame_id": frame_data["frame_info"]["frame_id"],
        "timestamp": frame_data["frame_info"]["timestamp"],
        "frame_base64": frame_base64,
        "detection_result": frame_data["detection_result"],
        "ocr_result": frame_data["ocr_result"]
    })

@app.get("/stream/frame/image")
async def get_latest_frame_image():
    """최신 프레임 이미지 (MJPEG 스트림)"""
    frame_data = stream_manager.get_latest_frame()
    if frame_data is None:
        return JSONResponse(content={"status": "no_frame"})
    
    frame = frame_data["frame"]
    _, buffer = cv2.imencode('.jpg', frame)
    
    return StreamingResponse(
        io.BytesIO(buffer.tobytes()),
        media_type="image/jpeg",
        headers={"Cache-Control": "no-cache"}
    )

@app.get("/stream/history")
async def get_detection_history():
    """탐지 히스토리 가져오기"""
    return JSONResponse(content={
        "total_frames": len(stream_manager.detection_history),
        "history": stream_manager.detection_history[-50:]  # 최근 50프레임만
    })

@app.websocket("/stream/ws")
async def websocket_stream(websocket: WebSocket):
    """WebSocket 실시간 스트림"""
    await websocket.accept()
    
    try:
        while True:
            frame_data = stream_manager.get_latest_frame()
            if frame_data:
                # 프레임을 base64로 인코딩
                frame = frame_data["frame"]
                _, buffer = cv2.imencode('.jpg', frame)
                frame_base64 = base64.b64encode(buffer).decode('utf-8')
                
                # WebSocket으로 전송
                await websocket.send_json({
                    "type": "frame",
                    "frame_id": frame_data["frame_info"]["frame_id"],
                    "timestamp": frame_data["frame_info"]["timestamp"],
                    "frame_base64": frame_base64,
                    "detection_result": frame_data["detection_result"],
                    "ocr_result": frame_data["ocr_result"]
                })
            
            await asyncio.sleep(0.033)  # 약 30 FPS
            
    except WebSocketDisconnect:
        print("WebSocket 연결이 끊어졌습니다.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
