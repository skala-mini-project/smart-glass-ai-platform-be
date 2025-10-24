# Vision AI 범용 모듈 - 협업용 베이스 시스템

## 🎯 프로젝트 개요

Physical AI 시대를 대비한 **범용성과 확장성을 갖춘 고정확도 실시간 Vision AI 모듈** 개발 프로젝트입니다.

### 핵심 목표
- **범용성**: 특정 도메인에 종속되지 않는 기본 모듈
- **정확성**: 기존 YOLO 대비 향상된 객체 인식 정확도
- **실시간성**: 30 FPS 이상의 실시간 처리 능력
- **확장성**: 다양한 응용 서비스로 확장 가능한 구조

## 🏗️ 현재 시스템 구조

```
backend/
├── main.py                          # FastAPI 메인 앱
├── requirements.txt                  # 통합 패키지 목록
├── rag_service/                     # 기존 RAG 서비스
│   ├── api/
│   │   ├── rag_router.py           # RAG API
│   │   └── health_router.py        # 헬스체크
│   └── ...
└── vision_service/                   # 🆕 Vision AI 모듈
    ├── __init__.py
    ├── core/
    │   ├── __init__.py
    │   └── detector.py              # YOLO 핵심 탐지 모듈
    └── api/
        ├── __init__.py
        └── vision_router.py        # Vision API 엔드포인트
```

## 🚀 빠른 시작

### 1. 환경 설정
```bash
cd backend
pip install -r requirements.txt
```

### 2. 서버 실행
```bash
python main.py
```

### 3. API 테스트
```bash
python test_vision_mockup.py
```

## 📡 API 엔드포인트

### Vision AI 서비스 (`/vision`)

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/vision/status` | GET | 서비스 상태 확인 |
| `/vision/detect/image` | POST | 단일 이미지 탐지 |
| `/vision/detect/upload` | POST | 업로드 파일 탐지 |
| `/vision/stream/start` | GET | 실시간 스트림 시작 |
| `/vision/stream/frame` | GET | 현재 프레임 조회 |
| `/vision/stream/stop` | GET | 스트림 종료 |
| `/vision/objects/history` | GET | 객체 히스토리 조회 |

### RAG 서비스 (`/rag`)
- 기존 템플릿 코드 기반
- 외부/내부 LLM 지원

## 🔧 현재 구현 상태 (목업)

### ✅ 구현 완료
- **Vision AI Core Module**: YOLO 기본 탐지
- **API 라우터**: 모든 엔드포인트 구현
- **JSON 출력 형식**: 표준화된 응답 구조
- **기존 RAG 통합**: 기존 서비스와 병행 운영

### 🚧 목업 기능
- **실제 웹캠 스트림**: 현재 더미 데이터
- **OCR 통합**: 향후 구현 예정
- **RAG 기반 정확도 향상**: Application Layer에서 구현
- **Multi-Modal 융합**: 고급 기능으로 확장

## 📊 출력 형식 예시

```json
{
  "frame_id": 1706094735234,
  "timestamp": "2025-01-24T14:32:15.234Z",
  "fps": 30.0,
  "resolution": [640, 480],
  "scene_context": "general",
  "objects": [
    {
      "id": 1,
      "label": "person",
      "confidence": 0.85,
      "bbox": {
        "x": 100,
        "y": 50,
        "width": 200,
        "height": 300
      },
      "center": [200, 200],
      "metadata": {
        "class_id": 0,
        "improved_by": []
      }
    }
  ],
  "processing_time_ms": 50.0,
  "model_version": "yolov8n",
  "status": "success"
}
```

## 🎯 다음 단계 (협업 계획)

### Phase 1: 실제 기능 구현 (1-2주)
1. **실제 웹캠 스트림 처리**
2. **OCR 통합** (EasyOCR/Tesseract)
3. **기본 성능 최적화**

### Phase 2: 정확도 향상 (2-3주)
1. **RAG 기반 정확도 향상**
2. **Scene Context 분석**
3. **Confidence 기반 보정**

### Phase 3: 고급 기능 (2-3주)
1. **Multi-Modal 융합**
2. **실시간 성능 최적화**
3. **데모 애플리케이션**

## 🛠️ 개발 환경

### 필수 패키지
- **FastAPI**: 웹 API 프레임워크
- **Ultralytics**: YOLO 모델
- **OpenCV**: 컴퓨터 비전
- **LangChain**: RAG 구현
- **FAISS**: 벡터 데이터베이스

### 권장 개발 도구
- **Python 3.8+**
- **CUDA** (GPU 가속, 선택사항)
- **Postman** (API 테스트)
- **VS Code** (개발 환경)

## 📝 협업 가이드

### 코드 스타일
- **PEP 8** 준수
- **타입 힌트** 사용
- **docstring** 작성
- **로깅** 활용

### Git 워크플로우
1. **feature/기능명** 브랜치 생성
2. **작은 단위**로 커밋
3. **Pull Request** 생성
4. **코드 리뷰** 후 머지

### 테스트
- **단위 테스트**: 각 모듈별 테스트
- **통합 테스트**: API 엔드포인트 테스트
- **성능 테스트**: 실시간 처리 성능 측정

## 🚨 주의사항

### 현재 목업 상태
- 실제 YOLO 모델이 로드되지 않을 수 있음
- 웹캠 스트림은 더미 데이터 사용
- 일부 기능은 시뮬레이션 상태

### 개발 시 고려사항
- **메모리 사용량** 모니터링
- **GPU 메모리** 관리
- **실시간 처리** 성능 유지

## 📞 문의 및 지원

프로젝트 관련 문의사항이나 기술적 지원이 필요한 경우:
- **이슈 등록**: GitHub Issues 활용
- **코드 리뷰**: Pull Request 활용
- **문서 업데이트**: README.md 수정

---

**🎉 협업 준비 완료! 함께 멋진 Vision AI 모듈을 만들어봅시다!**
