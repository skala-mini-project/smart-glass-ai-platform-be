# 전체 통합 테스트 스크립트
import asyncio
import cv2
import numpy as np
from datetime import datetime
import json
import os
from pathlib import Path

# 백엔드 모듈 import
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from vision_service.core.detector import VisionDetector
from rag_service.services.rag_service import RAGService
from vision_service.services.ocr_service import OCRService

class IntegrationTest:
    """전체 시스템 통합 테스트"""
    
    def __init__(self):
        self.vision_detector = VisionDetector()
        self.rag_service = RAGService()
        self.ocr_service = OCRService()
        self.test_results = []
    
    async def test_vision_detection(self):
        """Vision AI 테스트"""
        print("🔍 Vision AI 테스트 시작...")
        
        # 테스트 이미지 생성 (간단한 사각형)
        test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.rectangle(test_image, (100, 100), (300, 300), (0, 255, 0), 2)
        cv2.putText(test_image, "TEST", (150, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
        
        # 객체 탐지 실행
        result = self.vision_detector.detect_objects(test_image)
        
        print(f"✅ Vision AI 결과: {len(result['objects'])}개 객체 탐지")
        print(f"   - FPS: {result['fps']}")
        print(f"   - 해상도: {result['resolution']}")
        print(f"   - 처리시간: {result['processing_time_ms']}ms")
        
        return result
    
    async def test_ocr_service(self):
        """OCR 서비스 테스트"""
        print("\n📝 OCR 서비스 테스트 시작...")
        
        # 텍스트가 포함된 테스트 이미지 생성
        test_image = np.zeros((200, 400, 3), dtype=np.uint8)
        cv2.putText(test_image, "Hello World", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(test_image, "Test OCR", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # OCR 실행
        ocr_result = self.ocr_service.extract_text(test_image)
        
        print(f"✅ OCR 결과: {len(ocr_result['texts'])}개 텍스트 추출")
        for text in ocr_result['texts']:
            print(f"   - 텍스트: '{text['text']}' (신뢰도: {text['confidence']:.2f})")
        
        return ocr_result
    
    async def test_rag_service(self):
        """RAG 서비스 테스트"""
        print("\n🤖 RAG 서비스 테스트 시작...")
        
        # 테스트 쿼리
        test_query = "스마트 글래스에서 객체 인식은 어떻게 작동하나요?"
        
        try:
            rag_result = await self.rag_service.query(test_query)
            print(f"✅ RAG 결과: {len(rag_result.get('sources', []))}개 문서 검색")
            print(f"   - 응답: {rag_result.get('answer', '응답 없음')[:100]}...")
        except Exception as e:
            print(f"⚠️ RAG 서비스 오류: {e}")
            rag_result = {"answer": "RAG 서비스 테스트 실패", "sources": []}
        
        return rag_result
    
    async def test_webcam_simulation(self):
        """웹캠 시뮬레이션 테스트"""
        print("\n📹 웹캠 시뮬레이션 테스트 시작...")
        
        # 가상 웹캠 프레임 생성
        frames = []
        for i in range(5):  # 5프레임 시뮬레이션
            frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
            
            # 가상 객체 추가
            cv2.rectangle(frame, (50+i*10, 50+i*10), (150+i*10, 150+i*10), (0, 255, 0), 2)
            cv2.putText(frame, f"Frame {i+1}", (60+i*10, 80+i*10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            frames.append(frame)
        
        # 각 프레임 처리
        processed_frames = []
        for i, frame in enumerate(frames):
            result = self.vision_detector.detect_objects(frame)
            processed_frames.append({
                "frame_id": i+1,
                "objects_count": len(result['objects']),
                "processing_time": result['processing_time_ms']
            })
        
        print(f"✅ 웹캠 시뮬레이션 완료: {len(processed_frames)}프레임 처리")
        for frame_info in processed_frames:
            print(f"   - 프레임 {frame_info['frame_id']}: {frame_info['objects_count']}개 객체, {frame_info['processing_time']}ms")
        
        return processed_frames
    
    async def test_integrated_workflow(self):
        """통합 워크플로우 테스트"""
        print("\n🔄 통합 워크플로우 테스트 시작...")
        
        # 1. 이미지에서 객체 탐지
        test_image = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.rectangle(test_image, (100, 100), (300, 300), (0, 255, 0), 2)
        cv2.putText(test_image, "Smart Glass", (120, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # 2. Vision AI로 객체 탐지
        vision_result = self.vision_detector.detect_objects(test_image)
        
        # 3. OCR로 텍스트 추출
        ocr_result = self.ocr_service.extract_text(test_image)
        
        # 4. 탐지된 객체 정보로 RAG 쿼리 생성
        if vision_result['objects']:
            object_labels = [obj['label'] for obj in vision_result['objects']]
            rag_query = f"다음 객체들이 탐지되었습니다: {', '.join(object_labels)}. 이 객체들에 대해 설명해주세요."
            
            try:
                rag_result = await self.rag_service.query(rag_query)
                integrated_result = {
                    "vision": vision_result,
                    "ocr": ocr_result,
                    "rag": rag_result,
                    "workflow_status": "success"
                }
            except Exception as e:
                integrated_result = {
                    "vision": vision_result,
                    "ocr": ocr_result,
                    "rag": {"error": str(e)},
                    "workflow_status": "partial_success"
                }
        else:
            integrated_result = {
                "vision": vision_result,
                "ocr": ocr_result,
                "rag": {"message": "탐지된 객체 없음"},
                "workflow_status": "no_objects"
            }
        
        print(f"✅ 통합 워크플로우 완료: {integrated_result['workflow_status']}")
        return integrated_result
    
    async def run_all_tests(self):
        """모든 테스트 실행"""
        print("🚀 전체 시스템 통합 테스트 시작!")
        print("=" * 50)
        
        start_time = datetime.now()
        
        try:
            # 개별 테스트 실행
            vision_result = await self.test_vision_detection()
            ocr_result = await self.test_ocr_service()
            rag_result = await self.test_rag_service()
            webcam_result = await self.test_webcam_simulation()
            integrated_result = await self.test_integrated_workflow()
            
            # 결과 정리
            self.test_results = {
                "timestamp": datetime.now().isoformat(),
                "test_duration": (datetime.now() - start_time).total_seconds(),
                "vision_test": vision_result,
                "ocr_test": ocr_result,
                "rag_test": rag_result,
                "webcam_test": webcam_result,
                "integrated_test": integrated_result,
                "overall_status": "completed"
            }
            
            # 결과 저장
            with open("integration_test_results.json", "w", encoding="utf-8") as f:
                json.dump(self.test_results, f, ensure_ascii=False, indent=2)
            
            print("\n" + "=" * 50)
            print("🎉 전체 테스트 완료!")
            print(f"⏱️ 총 소요시간: {self.test_results['test_duration']:.2f}초")
            print("📄 결과 파일: integration_test_results.json")
            
        except Exception as e:
            print(f"\n❌ 테스트 실행 중 오류: {e}")
            self.test_results = {"error": str(e), "status": "failed"}

async def main():
    """메인 실행 함수"""
    tester = IntegrationTest()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
