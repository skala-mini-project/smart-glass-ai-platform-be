# RAG 서비스 개발 가이드 - Vision AI 프로젝트

## 🎯 RAG 담당자 역할 (김범준)

### 주요 책임
1. **Vision AI 정확도 향상을 위한 RAG 통합**
2. **기존 템플릿 코드 활용한 벡터 DB 구축**
3. **Vision 탐지 결과와 문서 검색 연동**
4. **Application Layer에서 RAG 활용**

## 📁 RAG 서비스 구조

```
rag_service/
├── api/
│   ├── rag_router.py      # /rag/query API 엔드포인트
│   └── health_router.py   # 헬스 체크
├── core/
│   └── config.py          # 설정 관리
├── models/
│   └── document.py        # 데이터 모델 정의
├── services/              # 🆕 Vision AI 연동 서비스
│   ├── enhancement_service.py  # Vision 정확도 향상
│   └── vision_rag_service.py   # Vision-RAG 통합
└── data/
    ├── documents/         # Vision 관련 문서 저장소
    └── embeddings/        # 생성된 임베딩 저장소
```

## 🔄 RAG 파이프라인 (Vision AI 통합)

### 기존 RAG 파이프라인
```
사용자 쿼리 → 문서 검색 → 컨텍스트 구성 → LLM 응답 생성
     ↓            ↓           ↓            ↓
  텍스트 입력   벡터 검색   관련 문서들   최종 답변
```

### 🆕 Vision AI 통합 파이프라인
```
Vision 탐지 결과 → 유사 케이스 검색 → 컨텍스트 증강 → 정확도 향상
     ↓                    ↓              ↓            ↓
  객체 정보 + 이미지    벡터 DB 검색    과거 데이터    개선된 레이블
     ↓                    ↓              ↓            ↓
  Confidence < 80%    유사 이미지들    관련 문서들    Confidence ↑
```

## 🛠️ 구현 단계

### Phase 1: 기본 인프라 ✅
- [x] FastAPI 라우터 설정
- [x] 데이터 모델 정의
- [x] 설정 관리 구조
- [x] **Vision AI 모듈과 통합**

### Phase 2: 템플릿 코드 활용 (진행 예정)
- [ ] **기존 템플릿 코드 분석 및 적용**
- [ ] FAISS 벡터 DB 설정 (template 기반)
- [ ] 외부/내부 LLM 연동 구조 활용
- [ ] 문서 임베딩 생성

### Phase 3: Vision-RAG 통합 (진행 예정)
- [ ] **Vision 탐지 결과와 RAG 연동**
- [ ] Confidence 기반 정확도 향상 로직
- [ ] 이미지 임베딩과 텍스트 임베딩 융합
- [ ] 유사 케이스 검색 시스템

### Phase 4: 고급 기능 (진행 예정)
- [ ] Scene Context 분석
- [ ] Temporal Context (시계열)
- [ ] Multi-Modal 융합
- [ ] 성능 최적화

## 📋 API 명세

### 기존 RAG API
```http
POST /rag/query
# 문서 검색 및 LLM 응답 생성

Request:
{
    "query": "안전모 착용 규정은?",
    "domain": "construction",
    "top_k": 5,
    "threshold": 0.7
}

Response:
{
    "answer": "건설현장안전관리규정 제15조에 따르면...",
    "sources": [
        {
            "document": "건설현장안전관리규정.pdf",
            "page": 15,
            "content": "관련 내용...",
            "similarity": 0.89
        }
    ],
    "processing_time": 1.2
}
```

### 🆕 Vision-RAG 통합 API (예정)
```http
POST /vision/enhance
# Vision 탐지 결과 정확도 향상

Request:
{
    "detection_result": {
        "label": "document",
        "confidence": 0.72,
        "bbox": [100, 50, 200, 300],
        "image_embedding": [0.1, 0.2, ...]
    },
    "context": "office"
}

Response:
{
    "enhanced_result": {
        "label": "contract_document",
        "confidence": 0.94,
        "improved_by": ["rag", "ocr"],
        "similar_cases": [
            {
                "label": "contract_document",
                "similarity": 0.89,
                "source": "legal_docs.pdf"
            }
        ]
    }
}
```

## 🔧 기술 스택

### 핵심 라이브러리 (템플릿 기반)
- **FastAPI**: API 서버
- **FAISS**: 벡터 데이터베이스 (템플릿에서 사용)
- **LangChain**: RAG 파이프라인 (템플릿에서 사용)
- **OpenAI**: 외부 LLM 서비스 (템플릿에서 사용)
- **Transformers**: 내부 LLM 서비스 (템플릿에서 사용)
- **PyPDF2**: PDF 파싱

### 🆕 Vision AI 통합 라이브러리
- **Ultralytics**: YOLO 모델
- **OpenCV**: 이미지 처리
- **EasyOCR**: OCR 서비스
- **Sentence-Transformers**: 이미지/텍스트 임베딩

### 설정 예시 (템플릿 기반)
```python
# rag_service/core/config.py
class Settings(BaseSettings):
    # 템플릿에서 사용하는 설정들
    vector_db_type: str = "faiss"
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    llm_provider: str = "openai"  # 또는 "internal"
    
    # Vision AI 통합 설정
    vision_enhancement_threshold: float = 0.8
    image_embedding_model: str = "clip-vit-base-patch32"
    rag_enabled: bool = True
```

## 📚 참고 자료

### Template 코드 활용 (핵심!)
- `template/4.벡앤드(fast_api)/rag_external-web_pdf_closed_llm.py` - **외부 LLM 기반 RAG**
- `template/4.벡앤드(fast_api)/rag_internal-dbms_vdb_open_llm.py` - **내부 LLM 기반 RAG**

### 주요 기능 (템플릿에서 가져올 것들)
1. **문서 청킹**: `RecursiveCharacterTextSplitter`
2. **벡터 검색**: FAISS 유사도 검색
3. **임베딩**: OpenAI 또는 HuggingFace 모델
4. **LLM 응답**: 프롬프트 템플릿 기반
5. **외부/내부 LLM 분리**: 이중 서버 구조

### 🆕 Vision AI 통합 방향
1. **기존 RAG 구조 재사용**: 템플릿 코드 기반
2. **Vision 결과와 연동**: Confidence 기반 정확도 향상
3. **이미지 임베딩 추가**: CLIP 모델 활용
4. **Application Layer**: Core Module과 분리

## 🚀 다음 작업

### 1. 템플릿 코드 분석 및 적용
   - **기존 템플릿 코드 상세 분석**
   - FAISS 벡터 DB 설정 (템플릿 기반)
   - 외부/내부 LLM 연동 구조 이해

### 2. Vision-RAG 통합 서비스 구현
   - **Vision 탐지 결과와 RAG 연동**
   - Confidence 기반 정확도 향상 로직
   - 이미지 임베딩과 텍스트 임베딩 융합

### 3. 고급 기능 개발
   - Scene Context 분석
   - Temporal Context (시계열)
   - Multi-Modal 융합

## ❓ 질문 및 지원

- **RAG 기술적 질문**: 김범준
- **템플릿 코드 활용**: 김범준
- **Vision AI 통합**: 김범준
- **전체 구조**: 김범준 (프로젝트 리드)

---

**참고**: 이 문서는 Vision AI 프로젝트의 RAG 통합 진행에 따라 업데이트됩니다.
