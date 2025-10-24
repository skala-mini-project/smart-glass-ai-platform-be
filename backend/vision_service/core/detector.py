# Vision AI Core Module
from ultralytics import YOLO
import cv2
import numpy as np
from typing import List, Dict, Any
import json
from datetime import datetime

class VisionDetector:
    """Vision AI 핵심 탐지 모듈 (목업 버전)"""
    
    def __init__(self):
        """YOLO 모델 초기화"""
        try:
            self.model = YOLO('yolov8n.pt')  # nano 버전 (빠른 처리)
            self.model_loaded = True
            print("✅ YOLO 모델 로드 완료")
        except Exception as e:
            print(f"❌ YOLO 모델 로드 실패: {e}")
            self.model_loaded = False
    
    def detect_objects(self, frame: np.ndarray) -> Dict[str, Any]:
        """실시간 객체 탐지 (목업)"""
        if not self.model_loaded:
            return self._get_mock_result()
        
        try:
            # YOLO 탐지 실행
            results = self.model(frame, verbose=False)
            
            # 결과 파싱
            detections = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # 바운딩 박스 좌표
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        confidence = box.conf[0].cpu().numpy()
                        class_id = int(box.cls[0].cpu().numpy())
                        class_name = self.model.names[class_id]
                        
                        detection = {
                            "id": len(detections) + 1,
                            "label": class_name,
                            "confidence": float(confidence),
                            "bbox": {
                                "x": int(x1),
                                "y": int(y1),
                                "width": int(x2 - x1),
                                "height": int(y2 - y1)
                            },
                            "center": [int((x1 + x2) / 2), int((y1 + y2) / 2)],
                            "metadata": {
                                "class_id": class_id,
                                "improved_by": []
                            }
                        }
                        detections.append(detection)
            
            return self._format_result(detections, frame.shape)
            
        except Exception as e:
            print(f"❌ 탐지 오류: {e}")
            return self._get_mock_result()
    
    def _format_result(self, detections: List[Dict], frame_shape: tuple) -> Dict[str, Any]:
        """결과 포맷팅"""
        return {
            "frame_id": int(datetime.now().timestamp() * 1000),
            "timestamp": datetime.now().isoformat(),
            "fps": 30.0,  # 목업용 고정값
            "resolution": [frame_shape[1], frame_shape[0]],  # [width, height]
            "scene_context": "general",
            "objects": detections,
            "processing_time_ms": 50.0,  # 목업용 고정값
            "model_version": "yolov8n",
            "status": "success"
        }
    
    def _get_mock_result(self) -> Dict[str, Any]:
        """모델 로드 실패시 목업 결과"""
        return {
            "frame_id": int(datetime.now().timestamp() * 1000),
            "timestamp": datetime.now().isoformat(),
            "fps": 30.0,
            "resolution": [640, 480],
            "scene_context": "general",
            "objects": [
                {
                    "id": 1,
                    "label": "person",
                    "confidence": 0.85,
                    "bbox": {"x": 100, "y": 50, "width": 200, "height": 300},
                    "center": [200, 200],
                    "metadata": {"class_id": 0, "improved_by": ["mock"]}
                }
            ],
            "processing_time_ms": 50.0,
            "model_version": "mock",
            "status": "mock_mode"
        }
