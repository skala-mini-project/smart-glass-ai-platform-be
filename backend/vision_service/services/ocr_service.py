# OCR 서비스 구현
import cv2
import numpy as np
from typing import Dict, List, Any
import json

class OCRService:
    """OCR 서비스 목업 구현"""
    
    def __init__(self):
        self.ocr_available = True
        print("✅ OCR 서비스 초기화 완료")
    
    def extract_text(self, image: np.ndarray) -> Dict[str, Any]:
        """텍스트 추출 (목업)"""
        try:
            # 간단한 텍스트 시뮬레이션
            height, width = image.shape[:2]
            
            # 이미지에서 텍스트 영역 감지 시뮬레이션
            texts = []
            
            # 가상의 텍스트 영역들
            text_regions = [
                {"text": "Hello World", "bbox": [50, 50, 200, 80], "confidence": 0.95},
                {"text": "Test OCR", "bbox": [50, 100, 150, 130], "confidence": 0.88},
                {"text": "Smart Glass", "bbox": [120, 200, 250, 230], "confidence": 0.92}
            ]
            
            for region in text_regions:
                # 실제 이미지 영역과 겹치는지 확인
                x, y, w, h = region["bbox"]
                if x < width and y < height and x + w <= width and y + h <= height:
                    texts.append({
                        "text": region["text"],
                        "bbox": region["bbox"],
                        "confidence": region["confidence"],
                        "language": "en"
                    })
            
            return {
                "texts": texts,
                "total_texts": len(texts),
                "processing_time_ms": 25.0,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "texts": [],
                "total_texts": 0,
                "processing_time_ms": 0.0,
                "status": "error",
                "error": str(e)
            }
