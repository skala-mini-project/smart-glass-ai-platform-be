# Smart Glass AI Platform - Backend

## 🎯 프로젝트 개요
Physical AI 시대를 대비한 **범용성과 확장성을 갖춘 고정확도 실시간 Vision AI 모듈** 개발 프로젝트입니다.

### 핵심 목표
- **범용성**: 특정 도메인에 종속되지 않는 기본 모듈
- **정확성**: 기존 YOLO 대비 향상된 객체 인식 정확도 (OCR, RAG, Multi-Modal 통합)
- **실시간성**: 30 FPS 이상의 실시간 처리 능력
- **확장성**: 다양한 응용 서비스로 확장 가능한 구조

## 🚀 주요 기능

### Vision AI Core Module
- **YOLO 기반 실시간 객체 탐지**: Ultralytics YOLOv8 활용
- **OCR 통합**: EasyOCR/Tesseract로 텍스트 정보 추출
- **표준화된 JSON 출력**: 다양한 응용 서비스 연동 가능

### 정확도 향상 모듈 (Application Layer)
- **RAG 기반 정확도 향상**: 기존 템플릿 코드 활용
- **Multi-Modal 융합**: Scene Context, Temporal Context 분석
- **Confidence 기반 보정**: 애매한 케이스 자동 개선

### 기존 RAG 서비스
- **문서 검색 및 LLM 응답**: OpenAI, Anthropic 등 다양한 LLM 지원
- **벡터 데이터베이스**: FAISS 기반 문서 임베딩 저장 및 유사도 검색

## 📁 프로젝트 구조
```
backend/
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
├── VISION_COLLABORATION_GUIDE.md  # 🆕 협업 가이드
├── RAG_DEVELOPMENT_GUIDE.md      # RAG 개발 가이드
└── TEAM_GUIDE.md                 # 팀 협업 가이드
```

## 🛠️ 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r backend/requirements.txt
```

### 2. 환경 변수 설정
```bash
cp backend/env.example backend/.env
# backend/.env 파일에서 API 키 등 설정
```

### 3. 서버 실행
```bash
cd backend
python main.py
# 또는
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 목업 테스트 실행
```bash
cd backend
python test_vision_mockup.py
```

## 📡 API 엔드포인트

### Health Check
- `GET /health/` - 기본 헬스 체크
- `GET /health/ready` - 서비스 준비 상태
- `GET /health/live` - 서비스 생존 상태

### 🆕 Vision AI Service
- `GET /vision/status` - Vision AI 서비스 상태 확인
- `POST /vision/detect/image` - 단일 이미지 객체 탐지
- `POST /vision/detect/upload` - 업로드 파일 탐지
- `GET /vision/stream/start` - 실시간 스트림 시작
- `GET /vision/stream/frame` - 현재 프레임 조회
- `GET /vision/stream/stop` - 스트림 종료
- `GET /vision/objects/history` - 객체 히스토리 조회

### RAG Service (기존)
- `POST /rag/query` - 문서 검색 및 LLM 응답 생성
- `GET /rag/status` - RAG 서비스 상태 확인

## 🚀 개발 계획

### ✅ 완료된 작업
- [x] **Vision AI Core Module 목업 구현**
- [x] **Vision API 라우터 구현**
- [x] **통합 requirements.txt 작성**
- [x] **목업 테스트 스크립트 작성**
- [x] **협업 가이드 문서화**

### 🔄 진행 예정 작업
- [ ] **실제 YOLO 모델 로딩 및 테스트**
- [ ] **OCR 서비스 통합** (EasyOCR/Tesseract)
- [ ] **실제 웹캠 스트림 처리**
- [ ] **RAG 기반 정확도 향상 모듈** (템플릿 코드 활용)
- [ ] **Multi-Modal 융합** (Scene/Temporal Context)
- [ ] **성능 최적화** (30 FPS 목표)
- [ ] **스마트 회의 어시스턴트 데모**
- [ ] **프론트엔드 실시간 시각화**

## 📚 참고 문서

- **[backend/VISION_COLLABORATION_GUIDE.md](./backend/VISION_COLLABORATION_GUIDE.md)**: 상세한 Vision AI 모듈 가이드
- **[backend/RAG_DEVELOPMENT_GUIDE.md](./backend/RAG_DEVELOPMENT_GUIDE.md)**: RAG 서비스 개발 가이드
- **[backend/TEAM_GUIDE.md](./backend/TEAM_GUIDE.md)**: 팀 협업 가이드
- **API 문서**: FastAPI 자동 생성 문서 (http://localhost:8000/docs)

## 🎯 프로젝트 비전

이 프로젝트는 Physical AI 시대의 핵심 기술인 **범용 Vision AI 모듈**을 개발하여, 스마트 글래스, 로봇, 자율주행 등 다양한 분야에서 활용할 수 있는 기반 기술을 제공합니다.

---

**🎉 협업 준비 완료! 함께 멋진 Vision AI 모듈을 만들어봅시다!**
