# 팀 협업 가이드 - Vision AI 범용 모듈 개발 프로젝트

## 🎯 프로젝트 개요

**Physical AI 시대를 대비한 범용성과 확장성을 갖춘 고정확도 실시간 Vision AI 모듈**

- **목표**: YOLO 기반 실시간 객체 탐지에 OCR, RAG, Multi-Modal 기술을 통합하여 정확도를 향상시킨 플랫폼 구축
- **핵심**: 범용성과 확장성을 갖춘 Vision AI Core Module + 다양한 응용 서비스
- **적용 분야**: 스마트 글래스, 로봇, 자율주행, 제조업, 의료, 리테일 등

## 👥 팀 역할 분담

| 담당자 | 역할 | 주요 작업 | API 엔드포인트 |
|--------|------|-----------|----------------|
| **김범준** | Vision AI Core | YOLO 객체 탐지, OCR 통합 | `/vision/detect`, `/vision/stream` |
| **김범준** | RAG 통합 | 정확도 향상을 위한 RAG 연동 | `/rag/query` |
| **팀원1** | OCR 서비스 | 텍스트 인식 및 추출 | `/vision/ocr` |
| **팀원2** | Multi-Modal | Scene Context, Temporal Context | `/vision/enhance` |
| **팀원3** | 데모 앱 | 스마트 회의 어시스턴트 | `/meeting/assistant` |
| **팀원4** | 프론트엔드 | 실시간 시각화, 웹 인터페이스 | - |
| **팀원5** | 성능 최적화 | 30 FPS 목표 달성, GPU 최적화 | - |

## 🏗️ 시스템 아키텍처

```
[실시간 카메라 입력] → [Vision AI Core Module] → [정확도 향상 모듈] → [표준 JSON 출력]
     ↓                        ↓                      ↓                    ↓
  웹캠/모바일            YOLO 객체 탐지         OCR + RAG + Multi-Modal   다양한 응용 서비스
     ↓                        ↓                      ↓                    ↓
 30 FPS 스트림          바운딩 박스, 레이블      Confidence 향상        스마트 회의, 제조, 의료
```

### 📊 데이터 처리 흐름

1. **입력**: 실시간 카메라 스트림 (30 FPS)
2. **Core Module**: YOLO 기반 기본 객체 탐지
3. **Enhancement**: OCR, RAG, Multi-Modal로 정확도 향상
4. **출력**: 표준화된 JSON 형식으로 결과 제공
5. **Application**: 다양한 응용 서비스로 확장

## 📁 백엔드 레포지토리 구조

```
ai-service/
├── main.py                    # FastAPI 앱 진입점
├── requirements.txt           # 통합 Python 의존성 (Vision AI + RAG)
├── rag_service/              # 기존 RAG 서비스
│   ├── api/
│   │   ├── rag_router.py     # /rag/query API
│   │   └── health_router.py  # 헬스 체크
│   ├── core/
│   │   └── config.py         # 설정 관리
│   ├── models/
│   │   └── document.py       # 데이터 모델
│   └── services/             # 비즈니스 로직
├── vision_service/           # 🆕 Vision AI 모듈
│   ├── core/
│   │   └── detector.py      # YOLO 핵심 탐지 모듈
│   ├── api/
│   │   └── vision_router.py # Vision API 엔드포인트
│   ├── services/             # OCR, Enhancement 서비스
│   └── models/              # Vision 데이터 모델
├── test_vision_mockup.py    # 🆕 목업 테스트 스크립트
└── VISION_COLLABORATION_GUIDE.md  # 🆕 협업 가이드
```

## 🔄 데이터 흐름

1. **입력**: 실시간 카메라 스트림 (웹캠, 모바일)
2. **처리**: 
   - Vision Core: YOLO 기반 객체 탐지
   - OCR: 텍스트 정보 추출 및 활용
   - RAG: 유사 케이스 검색으로 정확도 향상
   - Multi-Modal: Scene/Temporal Context 분석
3. **출력**: 표준화된 JSON 형식으로 탐지 결과 제공
4. **확장**: 다양한 응용 서비스로 활용 (회의, 제조, 의료 등)

## 🚀 개발 진행 상황

### ✅ 완료된 작업
- [x] 백엔드 레포지토리 기본 구조 생성
- [x] FastAPI 앱 설정 및 CORS 구성
- [x] RAG API 스켈레톤 코드
- [x] **Vision AI Core Module 목업 구현**
- [x] **Vision API 라우터 구현**
- [x] **통합 requirements.txt 작성**
- [x] **목업 테스트 스크립트 작성**
- [x] **협업 가이드 문서화**

### 🔄 진행 예정 작업
- [ ] **실제 YOLO 모델 로딩 및 테스트**
- [ ] **OCR 서비스 통합** (EasyOCR/Tesseract)
- [ ] **실제 웹캠 스트림 처리**
- [ ] **RAG 기반 정확도 향상 모듈**
- [ ] **Multi-Modal 융합** (Scene/Temporal Context)
- [ ] **성능 최적화** (30 FPS 목표)
- [ ] **스마트 회의 어시스턴트 데모**
- [ ] **프론트엔드 실시간 시각화**

## 📋 API 명세

### Vision AI Service (김범준)
```http
GET /vision/status
# Vision AI 서비스 상태 확인

POST /vision/detect/image
Content-Type: application/json
{
    "confidence_threshold": 0.5,
    "max_objects": 10
}

Response:
{
    "frame_id": 1706094735234,
    "timestamp": "2025-01-24T14:32:15.234Z",
    "fps": 30.0,
    "resolution": [640, 480],
    "objects": [
        {
            "id": 1,
            "label": "person",
            "confidence": 0.85,
            "bbox": {"x": 100, "y": 50, "width": 200, "height": 300},
            "center": [200, 200],
            "metadata": {"class_id": 0, "improved_by": []}
        }
    ],
    "processing_time_ms": 50.0,
    "model_version": "yolov8n",
    "status": "success"
}
```

### RAG Service (기존)
```http
POST /rag/query
Content-Type: application/json
{
    "query": "안전모 착용 규정은?",
    "domain": "construction",
    "top_k": 5,
    "threshold": 0.7
}
```

### Health Check
```http
GET /health/
GET /health/ready
GET /health/live
```

## 🛠️ 개발 환경 설정

### 1. 레포지토리 클론
```bash
git clone [repository-url]
cd ai-service/backend
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
```bash
cp env.example .env
# .env 파일에서 API 키 등 설정
```

### 4. 서버 실행
```bash
python main.py
# 또는
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 목업 테스트 실행
```bash
python test_vision_mockup.py
```

## 📞 협업 방식

1. **브랜치 전략**: 각 담당자별 feature 브랜치 생성
2. **커밋 메시지**: `[담당자] 기능: 설명` 형식
3. **PR 리뷰**: 최소 1명 이상 리뷰 후 머지
4. **문서화**: API 변경 시 README 업데이트 필수
5. **테스트**: 새로운 기능 추가 시 테스트 코드 작성

## ❓ 질문 및 지원

- **Vision AI 관련**: 김범준
- **RAG 통합**: 김범준
- **전체 구조**: 김범준 (프로젝트 리드)
- **프론트엔드**: 팀원4

## 📚 참고 문서

- **VISION_COLLABORATION_GUIDE.md**: 상세한 Vision AI 모듈 가이드
- **API 문서**: FastAPI 자동 생성 문서 (http://localhost:8000/docs)

---

**참고**: 이 문서는 프로젝트 진행에 따라 지속적으로 업데이트됩니다.
