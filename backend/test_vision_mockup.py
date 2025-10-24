#!/usr/bin/env python3
"""
Vision AI 목업 테스트 스크립트
협업용 베이스 시스템 테스트
"""

import requests
import json
import time
from datetime import datetime

# API 베이스 URL
BASE_URL = "http://localhost:8000"

def test_health():
    """헬스체크 테스트"""
    print("🔍 헬스체크 테스트...")
    try:
        response = requests.get(f"{BASE_URL}/health/")
        print(f"✅ 헬스체크 성공: {response.status_code}")
        print(f"   응답: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ 헬스체크 실패: {e}")
        return False

def test_rag_status():
    """RAG 서비스 상태 테스트"""
    print("\n🔍 RAG 서비스 상태 테스트...")
    try:
        response = requests.get(f"{BASE_URL}/rag/status")
        print(f"✅ RAG 상태 확인 성공: {response.status_code}")
        print(f"   응답: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ RAG 상태 확인 실패: {e}")
        return False

def test_vision_status():
    """Vision AI 서비스 상태 테스트"""
    print("\n🔍 Vision AI 서비스 상태 테스트...")
    try:
        response = requests.get(f"{BASE_URL}/vision/status")
        print(f"✅ Vision AI 상태 확인 성공: {response.status_code}")
        print(f"   응답: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Vision AI 상태 확인 실패: {e}")
        return False

def test_vision_detection():
    """Vision AI 객체 탐지 테스트"""
    print("\n🔍 Vision AI 객체 탐지 테스트...")
    try:
        # 목업 이미지 탐지 요청
        request_data = {
            "confidence_threshold": 0.5,
            "max_objects": 5
        }
        
        response = requests.post(
            f"{BASE_URL}/vision/detect/image",
            json=request_data
        )
        
        print(f"✅ 객체 탐지 성공: {response.status_code}")
        result = response.json()
        
        print(f"   프레임 ID: {result['frame_id']}")
        print(f"   탐지된 객체 수: {len(result['objects'])}")
        print(f"   처리 시간: {result['processing_time_ms']}ms")
        print(f"   모델 버전: {result['model_version']}")
        
        if result['objects']:
            print("   탐지된 객체들:")
            for obj in result['objects']:
                print(f"     - {obj['label']} (신뢰도: {obj['confidence']:.2f})")
        
        return True
        
    except Exception as e:
        print(f"❌ 객체 탐지 실패: {e}")
        return False

def test_stream_operations():
    """스트림 작업 테스트"""
    print("\n🔍 스트림 작업 테스트...")
    try:
        # 스트림 시작
        response = requests.get(f"{BASE_URL}/vision/stream/start")
        print(f"✅ 스트림 시작 성공: {response.status_code}")
        start_result = response.json()
        print(f"   스트림 ID: {start_result['stream_id']}")
        
        # 현재 프레임 조회
        time.sleep(1)
        response = requests.get(f"{BASE_URL}/vision/stream/frame")
        print(f"✅ 프레임 조회 성공: {response.status_code}")
        frame_result = response.json()
        print(f"   프레임 ID: {frame_result['frame_id']}")
        
        # 스트림 종료
        response = requests.get(f"{BASE_URL}/vision/stream/stop")
        print(f"✅ 스트림 종료 성공: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ 스트림 작업 실패: {e}")
        return False

def test_object_history():
    """객체 히스토리 테스트"""
    print("\n🔍 객체 히스토리 테스트...")
    try:
        response = requests.get(f"{BASE_URL}/vision/objects/history?limit=3")
        print(f"✅ 히스토리 조회 성공: {response.status_code}")
        history_result = response.json()
        print(f"   히스토리 항목 수: {history_result['total_count']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 히스토리 조회 실패: {e}")
        return False

def main():
    """메인 테스트 함수"""
    print("=" * 60)
    print("🚀 Vision AI 목업 시스템 테스트 시작")
    print("=" * 60)
    
    # 서버가 실행 중인지 확인
    print(f"📡 테스트 대상 서버: {BASE_URL}")
    print(f"⏰ 테스트 시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 테스트 실행
    tests = [
        ("헬스체크", test_health),
        ("RAG 서비스", test_rag_status),
        ("Vision AI 서비스", test_vision_status),
        ("객체 탐지", test_vision_detection),
        ("스트림 작업", test_stream_operations),
        ("객체 히스토리", test_object_history)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} 테스트 중 예외 발생: {e}")
            results.append((test_name, False))
    
    # 결과 요약
    print("\n" + "=" * 60)
    print("📊 테스트 결과 요약")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ 통과" if success else "❌ 실패"
        print(f"   {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 전체 결과: {passed}/{total} 테스트 통과")
    
    if passed == total:
        print("🎉 모든 테스트가 성공했습니다! 협업 준비 완료!")
    else:
        print("⚠️  일부 테스트가 실패했습니다. 서버 상태를 확인해주세요.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
