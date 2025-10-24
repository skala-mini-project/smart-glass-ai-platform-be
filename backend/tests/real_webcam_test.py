# 실제 웹캠 통합 테스트
import cv2
import numpy as np
from datetime import datetime
import json
import asyncio
import sys
import os

# 백엔드 모듈 import
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from vision_service.core.detector import VisionDetector
from rag_service.services.rag_service import RAGService
from vision_service.services.ocr_service import OCRService

class RealWebcamTest:
    """실제 웹캠을 사용한 통합 테스트"""
    
    def __init__(self):
        self.vision_detector = VisionDetector()
        self.rag_service = RAGService()
        self.ocr_service = OCRService()
        self.cap = None
        self.frame_count = 0
        self.detection_history = []
    
    def initialize_webcam(self):
        """웹캠 초기화"""
        print("📹 웹캠 초기화 중...")
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            print("❌ 웹캠을 열 수 없습니다!")
            return False
        
        # 웹캠 설정
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        print("✅ 웹캠 초기화 완료!")
        return True
    
    def process_frame(self, frame):
        """프레임 처리"""
        self.frame_count += 1
        
        # 1. 객체 탐지
        detection_result = self.vision_detector.detect_objects(frame)
        
        # 2. OCR 텍스트 추출
        ocr_result = self.ocr_service.extract_text(frame)
        
        # 3. 결과 시각화
        processed_frame = self.visualize_results(frame, detection_result, ocr_result)
        
        # 4. 히스토리 저장
        frame_info = {
            "frame_id": self.frame_count,
            "timestamp": datetime.now().isoformat(),
            "detections": len(detection_result['objects']),
            "texts": len(ocr_result['texts']),
            "objects": detection_result['objects'],
            "texts": ocr_result['texts']
        }
        self.detection_history.append(frame_info)
        
        return processed_frame, detection_result, ocr_result
    
    def visualize_results(self, frame, detection_result, ocr_result):
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
    
    async def run_realtime_test(self, duration_seconds=30):
        """실시간 테스트 실행"""
        if not self.initialize_webcam():
            return
        
        print(f"🚀 실시간 테스트 시작! ({duration_seconds}초간 실행)")
        print("📝 'q' 키를 누르면 종료됩니다.")
        print("=" * 50)
        
        start_time = datetime.now()
        
        try:
            while True:
                # 프레임 읽기
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ 프레임을 읽을 수 없습니다!")
                    break
                
                # 프레임 처리
                processed_frame, detection_result, ocr_result = self.process_frame(frame)
                
                # 화면에 표시
                cv2.imshow('Real-time Vision AI Test', processed_frame)
                
                # 키 입력 확인
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("🛑 사용자가 종료를 요청했습니다.")
                    break
                
                # 시간 체크
                elapsed = (datetime.now() - start_time).total_seconds()
                if elapsed >= duration_seconds:
                    print(f"⏰ {duration_seconds}초가 지나 종료합니다.")
                    break
                
                # 주기적으로 결과 출력
                if self.frame_count % 30 == 0:  # 30프레임마다
                    print(f"📊 프레임 {self.frame_count}: {len(detection_result['objects'])}개 객체, {len(ocr_result['texts'])}개 텍스트")
        
        except KeyboardInterrupt:
            print("\n🛑 사용자가 중단했습니다.")
        
        finally:
            self.cleanup()
            self.save_results()
    
    def cleanup(self):
        """정리 작업"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("✅ 리소스 정리 완료")
    
    def save_results(self):
        """결과 저장"""
        results = {
            "test_type": "real_webcam_test",
            "timestamp": datetime.now().isoformat(),
            "total_frames": self.frame_count,
            "detection_history": self.detection_history,
            "summary": {
                "total_objects_detected": sum(len(frame['objects']) for frame in self.detection_history),
                "total_texts_extracted": sum(len(frame['texts']) for frame in self.detection_history),
                "average_objects_per_frame": sum(len(frame['objects']) for frame in self.detection_history) / max(self.frame_count, 1),
                "average_texts_per_frame": sum(len(frame['texts']) for frame in self.detection_history) / max(self.frame_count, 1)
            }
        }
        
        with open("real_webcam_test_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print("📄 결과 파일 저장: real_webcam_test_results.json")
        print(f"📊 총 {self.frame_count}프레임 처리 완료!")
        print(f"🎯 평균 {results['summary']['average_objects_per_frame']:.2f}개 객체/프레임")
        print(f"📝 평균 {results['summary']['average_texts_per_frame']:.2f}개 텍스트/프레임")

async def main():
    """메인 실행 함수"""
    tester = RealWebcamTest()
    await tester.run_realtime_test(duration_seconds=30)

if __name__ == "__main__":
    asyncio.run(main())
