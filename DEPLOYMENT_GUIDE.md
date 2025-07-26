# 🚀 헬스장 시스템 배포 가이드

## 📋 배포 준비 상태 ✅

현재 프로젝트는 **즉시 배포 가능**한 상태입니다!

### 준비된 파일들
- ✅ `requirements.txt` - 의존성 목록
- ✅ `src/main.py` - FastAPI 애플리케이션
- ✅ `templates/` - HTML 템플릿
- ✅ 완전한 기능 구현
- ✅ 테스트 완료 (10/10 통과)

---

## 🌐 배포 옵션 비교

| 플랫폼 | 가격 | 난이도 | 특징 | 추천도 |
|--------|------|--------|------|--------|
| **Render** | 무료 | ⭐ | 자동 HTTPS, 쉬운 설정 | ⭐⭐⭐⭐⭐ |
| **Railway** | 무료(제한) | ⭐⭐ | GitHub 연동 | ⭐⭐⭐⭐ |
| **DigitalOcean** | $5/월 | ⭐⭐ | 안정적 성능 | ⭐⭐⭐⭐ |
| **AWS Lightsail** | $3.50/월 | ⭐⭐⭐ | 확장성 좋음 | ⭐⭐⭐ |

---

## 🎯 추천: Render.com 무료 배포

### 1. **사전 준비**

#### 1.1 GitHub 리퍼지토리 생성
```bash
# Git 초기화 (프로젝트 폴더에서)
git init
git add .
git commit -m "Initial commit: 헬스장 관리 시스템"

# GitHub에 push (리퍼지토리 생성 후)
git remote add origin https://github.com/[사용자명]/[리퍼지토리명].git
git push -u origin main
```

#### 1.2 배포용 설정 파일 생성

**파일**: `render.yaml` (프로젝트 루트에 생성)
```yaml
services:
  - type: web
    name: gym-management-system
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn src.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.12.0
```

### 2. **Render.com 배포 단계**

#### 2.1 계정 생성
1. [Render.com](https://render.com) 접속
2. GitHub 계정으로 회원가입
3. GitHub 연동 승인

#### 2.2 서비스 생성
1. **"New +"** 클릭 → **"Web Service"** 선택
2. GitHub 리퍼지토리 연결
3. 설정 입력:
   - **Name**: `gym-management-system`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

#### 2.3 배포 완료
- 자동 빌드 시작 (3-5분 소요)
- 배포 완료 시 URL 제공: `https://gym-management-system.onrender.com`

### 3. **접속 확인**
- **메인 페이지**: `https://[앱이름].onrender.com`
- **관리자 모드**: `https://[앱이름].onrender.com/admin`
- **API 문서**: `https://[앱이름].onrender.com/docs`

---

## 🔧 배포를 위한 코드 수정 (필요시)

### 1. **환경 변수 지원 추가**

**파일**: `src/database/database.py`
```python
import os

# 환경에 따른 데이터베이스 설정
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(DATABASE_URL)
```

### 2. **CORS 설정 (필요시)**

**파일**: `src/main.py`
```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(...)

# CORS 설정 (다른 도메인에서 접근 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 구체적 도메인 지정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. **Dockerfile** (Docker 배포용)

**파일**: `Dockerfile`
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🌟 다른 배포 방법들

### Railway.app 배포
1. [Railway.app](https://railway.app) 접속
2. GitHub 연동 후 리퍼지토리 선택
3. 자동 배포 (설정 불필요)

### Heroku 배포 (유료)
1. `Procfile` 생성:
   ```
   web: uvicorn src.main:app --host 0.0.0.0 --port $PORT
   ```
2. Heroku CLI로 배포

### DigitalOcean App Platform
1. GitHub 연동
2. Python 앱으로 설정
3. 빌드/실행 명령어 설정

---

## 📱 배포 후 사용법

### 1. **헬스장 직원용**
```
https://[앱이름].onrender.com
```
- 전화번호 뒷자리 4자리 입력
- 즉시 회원 확인 및 환영 메시지

### 2. **관리자용**
```
https://[앱이름].onrender.com/admin
```
- 회원 등록/수정/삭제
- 전체 회원 관리

### 3. **개발자/테스트용**
```
https://[앱이름].onrender.com/docs
```
- Swagger UI로 API 테스트

---

## ⚠️ 운영 시 주의사항

### 1. **데이터 백업**
- SQLite 파일은 서버 재시작 시 초기화될 수 있음
- 중요한 데이터는 별도 백업 필요

### 2. **성능 최적화**
- 무료 플랜은 비활성 시 슬립 모드
- 첫 접속 시 10-30초 로딩 시간

### 3. **보안 강화**
- 관리자 페이지 인증 추가 고려
- HTTPS 자동 적용됨 (Render 기본)

### 4. **모니터링**
- Render 대시보드에서 로그 확인 가능
- 오류 발생 시 이메일 알림

---

## 🎯 배포 성공 체크리스트

- [ ] GitHub 리퍼지토리 생성 및 푸시
- [ ] Render.com 계정 생성
- [ ] 웹 서비스 생성 및 설정
- [ ] 빌드 성공 확인
- [ ] 배포된 URL 접속 테스트
- [ ] 메인 페이지 동작 확인
- [ ] 관리자 페이지 동작 확인
- [ ] 출입 확인 기능 테스트
- [ ] 회원 등록 기능 테스트

---

## 💡 배포 후 개선 사항

### 1. **커스텀 도메인** (유료)
- `gym.yourdomain.com` 같은 전용 도메인

### 2. **데이터베이스 업그레이드**
- PostgreSQL로 마이그레이션
- 데이터 영구 보존

### 3. **인증 시스템**
- 관리자 로그인 기능
- 권한 관리

### 4. **알림 기능**
- 만료 임박 회원 이메일 알림
- SMS 알림 연동

---

**배포 완료 예상 시간**: 30분  
**총 비용**: 무료 (Render 기본 플랜)  
**접근성**: 전 세계 어디서나 접속 가능 🌍