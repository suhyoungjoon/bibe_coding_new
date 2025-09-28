# 🌐 바이브 코딩 프로젝트 웹 배포 가이드

> **로컬 개발 환경을 웹 서비스로 배포하는 완전한 가이드**

## 📋 목차
- [배포 옵션 비교](#배포-옵션-비교)
- [Railway 배포 (추천)](#railway-배포-추천)
- [Render 배포](#render-배포)
- [Heroku 배포](#heroku-배포)
- [AWS 배포](#aws-배포)
- [배포 전 준비사항](#배포-전-준비사항)
- [환경 설정](#환경-설정)
- [도메인 및 SSL](#도메인-및-ssl)
- [모니터링 및 로깅](#모니터링-및-로깅)
- [비용 분석](#비용-분석)
- [트러블슈팅](#트러블슈팅)

---

## 🎯 배포 옵션 비교

### **📊 상세 비교표**

| 서비스 | 난이도 | 무료 티어 | 유료 플랜 | 성능 | 관리 편의성 | 추천도 | 특징 |
|--------|--------|-----------|-----------|------|-------------|--------|------|
| **Railway** | ⭐⭐ | 500시간/월 | $5/월 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | GitHub 연동, 자동 배포 |
| **Render** | ⭐⭐ | 750시간/월 | $7/월 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 무료 SSL, 자동 스케일링 |
| **Heroku** | ⭐⭐ | 550시간/월 | $7/월 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 전통적인 PaaS |
| **AWS EC2** | ⭐⭐⭐⭐ | 12개월 무료 | $10-50/월 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | 완전한 제어권 |
| **Google Cloud** | ⭐⭐⭐⭐ | $300 크레딧 | $10-50/월 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | 고성능 인프라 |
| **DigitalOcean** | ⭐⭐⭐ | $200 크레딧 | $6/월 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 간단한 VPS |

### **🎯 추천 순위**

1. **🥇 Railway** - 가장 간단하고 GitHub 연동 완벽
2. **🥈 Render** - 무료 티어가 넉넉하고 안정적
3. **🥉 Heroku** - 전통적이고 검증된 서비스
4. **AWS/Google Cloud** - 대규모 서비스용
5. **DigitalOcean** - 중간 규모 서비스용

---

## 🚀 Railway 배포 (추천)

### **Railway를 추천하는 이유**
- ✅ **GitHub 연동**: 코드 푸시 시 자동 배포
- ✅ **환경 변수 관리**: 보안 정보 안전하게 관리
- ✅ **PostgreSQL 지원**: 데이터베이스 자동 제공
- ✅ **Docker 지원**: 복잡한 설정 불필요
- ✅ **무료 티어**: 월 500시간 무료 사용
- ✅ **자동 HTTPS**: SSL 인증서 자동 발급

### **Railway 배포 단계**

#### **Step 1: Railway 계정 생성**
1. **Railway.app** 접속
2. **"Login with GitHub"** 클릭
3. GitHub 권한 승인

#### **Step 2: 프로젝트 생성**
1. **"New Project"** 클릭
2. **"Deploy from GitHub repo"** 선택
3. **bibe_coding_new** 저장소 선택
4. **"Deploy Now"** 클릭

#### **Step 3: 환경 변수 설정**
Railway 대시보드 → Settings → Variables에서 다음 설정:

```env
# Azure OpenAI 설정
AZURE_OPENAI_API_KEY=Es9HkLmQUt3bbIf8V2mXtjFGrdUKxSouNBI6lF0eZ3T5tnjJhIkIJQQJ99BGACYeBjFXJ3w3AAABACOGtcwu
AZURE_OPENAI_ENDPOINT=https://openai-syj.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-06-01
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small

# 애플리케이션 설정
ENVIRONMENT=production
PORT=8000
HOST=0.0.0.0
DEBUG=False

# 데이터베이스 설정 (Railway PostgreSQL 사용 시)
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

#### **Step 4: PostgreSQL 데이터베이스 추가**
1. Railway 대시보드에서 **"New"** 클릭
2. **"Database"** → **"PostgreSQL"** 선택
3. 자동으로 애플리케이션과 연결됨

#### **Step 5: 도메인 설정**
1. **Settings** → **Domains**에서 커스텀 도메인 설정 가능
2. Railway 자동 도메인: `https://bibe-coding-production.railway.app`

### **Railway 설정 파일**

#### **railway.json**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "python main.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10,
    "healthcheckPath": "/api/v1/health",
    "healthcheckTimeout": 300,
    "sleepApplication": false,
    "sleepApplicationTimeout": 300
  }
}
```

---

## 🎨 Render 배포

### **Render 배포 단계**

#### **Step 1: Render 계정 생성**
1. **render.com** 접속
2. **"Get Started for Free"** 클릭
3. GitHub으로 로그인

#### **Step 2: Web Service 생성**
1. **"New +"** → **"Web Service"** 클릭
2. GitHub 저장소 연결
3. **"bibe_coding_new"** 선택

#### **Step 3: 서비스 설정**
```yaml
Name: bibe-coding
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: python main.py
Plan: Free (또는 Starter $7/월)
```

#### **Step 4: 환경 변수 설정**
Render 대시보드 → Environment에서 설정:

```env
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=your_endpoint_here
AZURE_OPENAI_API_VERSION=2024-06-01
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
ENVIRONMENT=production
```

#### **Step 5: PostgreSQL 데이터베이스 추가**
1. **"New +"** → **"PostgreSQL"** 클릭
2. 데이터베이스 생성
3. **Internal Database URL** 복사하여 환경 변수에 추가

---

## 🟣 Heroku 배포

### **Heroku 배포 단계**

#### **Step 1: Heroku CLI 설치**
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows
# Heroku CLI 다운로드 및 설치

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

#### **Step 2: Heroku 로그인 및 앱 생성**
```bash
heroku login
heroku create bibe-coding-app
```

#### **Step 3: PostgreSQL 추가**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

#### **Step 4: 환경 변수 설정**
```bash
heroku config:set AZURE_OPENAI_API_KEY=your_key_here
heroku config:set AZURE_OPENAI_ENDPOINT=your_endpoint_here
heroku config:set AZURE_OPENAI_API_VERSION=2024-06-01
heroku config:set AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
heroku config:set AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
heroku config:set ENVIRONMENT=production
```

#### **Step 5: 배포**
```bash
git push heroku main
```

### **Heroku 설정 파일**

#### **Procfile**
```
web: python main.py
```

#### **runtime.txt**
```
python-3.10.11
```

---

## ☁️ AWS 배포

### **AWS EC2 배포 (고급)**

#### **Step 1: EC2 인스턴스 생성**
1. AWS Console → EC2 → Launch Instance
2. **Ubuntu Server 22.04 LTS** 선택
3. **t2.micro** (무료 티어) 또는 **t3.small** 선택
4. Security Group에서 포트 22, 80, 443, 8000 열기

#### **Step 2: 서버 설정**
```bash
# 서버 접속
ssh -i your-key.pem ubuntu@your-ec2-ip

# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# Python 3.10 설치
sudo apt install python3.10 python3.10-venv python3-pip -y

# Git 설치
sudo apt install git -y

# 프로젝트 클론
git clone https://github.com/suhyoungjoon/bibe_coding_new.git
cd bibe_coding_new

# 가상환경 생성 및 활성화
python3.10 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

#### **Step 3: Nginx 설정**
```bash
# Nginx 설치
sudo apt install nginx -y

# Nginx 설정 파일 생성
sudo nano /etc/nginx/sites-available/bibe-coding
```

#### **Nginx 설정 파일**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### **Step 4: SSL 인증서 설정**
```bash
# Certbot 설치
sudo apt install certbot python3-certbot-nginx -y

# SSL 인증서 발급
sudo certbot --nginx -d your-domain.com
```

---

## ⚙️ 배포 전 준비사항

### **1. 코드 수정 필요사항**

#### **환경 변수 처리 개선**
```python
# app/core/config.py 수정
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 기존 설정...
    
    # 배포 환경 감지
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = os.getenv("HOST", "127.0.0.1")
    
    # CORS 설정
    ALLOWED_ORIGINS: list = [
        "https://*.railway.app",
        "https://*.render.com",
        "https://*.herokuapp.com",
        "https://your-domain.com",
        "http://localhost:3000",
        "http://localhost:8000"
    ] if ENVIRONMENT == "production" else ["*"]
    
    # 데이터베이스 URL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    class Config:
        env_file = ".env"
```

#### **CORS 설정 강화**
```python
# main.py 수정
from app.core.config import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

#### **서버 실행 설정**
```python
# main.py 수정
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level="info"
    )
```

### **2. Docker 설정 (Railway/Render용)**

#### **Dockerfile**
```dockerfile
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 포트 노출
EXPOSE 8000

# 헬스체크
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# 애플리케이션 실행
CMD ["python", "main.py"]
```

#### **.dockerignore**
```dockerignore
# Git
.git
.gitignore
.github

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/

# Test files
test_*.py
*_test.py
test_*.txt

# Documentation
*.md
docs/

# Temporary files
temp/
tmp/
*.tmp
```

---

## 🔧 환경 설정

### **환경별 설정 파일**

#### **개발 환경 (.env.development)**
```env
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=DEBUG
HOST=127.0.0.1
PORT=8000
```

#### **스테이징 환경 (.env.staging)**
```env
ENVIRONMENT=staging
DEBUG=False
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
```

#### **프로덕션 환경 (.env.production)**
```env
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=WARNING
HOST=0.0.0.0
PORT=8000
```

### **보안 설정**

#### **환경 변수 검증**
```python
# app/core/config.py
from pydantic import validator

class Settings(BaseSettings):
    # 기존 설정...
    
    @validator('AZURE_OPENAI_API_KEY')
    def validate_azure_key(cls, v):
        if not v or len(v) < 10:
            raise ValueError('Azure OpenAI API Key is required')
        return v
    
    @validator('ENVIRONMENT')
    def validate_environment(cls, v):
        allowed_envs = ['development', 'staging', 'production']
        if v not in allowed_envs:
            raise ValueError(f'Environment must be one of {allowed_envs}')
        return v
```

---

## 🌐 도메인 및 SSL

### **커스텀 도메인 설정**

#### **Railway에서 도메인 설정**
1. Railway 대시보드 → Settings → Domains
2. **"Custom Domain"** 클릭
3. 도메인 입력: `your-domain.com`
4. DNS 설정에서 CNAME 레코드 추가:
   ```
   Type: CNAME
   Name: www
   Value: your-app.railway.app
   ```

#### **Render에서 도메인 설정**
1. Render 대시보드 → Settings → Custom Domains
2. 도메인 추가
3. DNS 설정에서 CNAME 레코드 추가

### **SSL 인증서**
- **Railway**: 자동으로 Let's Encrypt SSL 발급
- **Render**: 자동으로 SSL 활성화
- **Heroku**: 자동으로 SSL 제공
- **AWS**: Certbot으로 Let's Encrypt 설정

---

## 📊 모니터링 및 로깅

### **Railway 모니터링**
- **Metrics**: CPU, 메모리, 네트워크 사용량
- **Logs**: 실시간 로그 스트리밍
- **Deployments**: 배포 히스토리

### **Render 모니터링**
- **Metrics**: 성능 메트릭
- **Logs**: 애플리케이션 로그
- **Health Checks**: 자동 헬스체크

### **로깅 설정**
```python
# app/core/config.py
import logging

class Settings(BaseSettings):
    # 기존 설정...
    
    LOG_LEVEL: str = "INFO"
    
    def setup_logging(self):
        logging.basicConfig(
            level=getattr(logging, self.LOG_LEVEL.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('app.log') if self.ENVIRONMENT == "production" else logging.NullHandler()
            ]
        )
```

---

## 💰 비용 분석

### **월 예상 비용**

| 서비스 | 무료 티어 | 유료 플랜 | 예상 사용량 | 총 비용 |
|--------|-----------|-----------|-------------|---------|
| **Railway** | 500시간 | $5/월 | 중간 사용 | $5/월 |
| **Render** | 750시간 | $7/월 | 중간 사용 | $7/월 |
| **Heroku** | 550시간 | $7/월 | 중간 사용 | $7/월 |
| **AWS EC2** | 12개월 무료 | $10-20/월 | 높은 사용 | $10-20/월 |

### **추가 비용**
- **Azure OpenAI**: $5-20/월 (사용량에 따라)
- **도메인**: $10-15/년
- **SSL**: 대부분 무료 (Let's Encrypt)

### **총 예상 비용**
- **Railway + Azure OpenAI**: $10-25/월
- **Render + Azure OpenAI**: $12-27/월
- **Heroku + Azure OpenAI**: $12-27/월

---

## 🔧 트러블슈팅

### **자주 발생하는 문제들**

#### **1. 환경 변수 문제**
```bash
# 문제: 환경 변수가 제대로 로드되지 않음
# 해결: 환경 변수 이름 확인 및 대소문자 구분
echo $AZURE_OPENAI_API_KEY
```

#### **2. 포트 문제**
```python
# 문제: 포트가 이미 사용 중
# 해결: 환경 변수로 포트 설정
PORT = int(os.getenv("PORT", 8000))
```

#### **3. CORS 문제**
```python
# 문제: CORS 오류
# 해결: 허용된 도메인에 배포 URL 추가
ALLOWED_ORIGINS = [
    "https://your-app.railway.app",
    "https://your-domain.com"
]
```

#### **4. 데이터베이스 연결 문제**
```python
# 문제: PostgreSQL 연결 실패
# 해결: DATABASE_URL 환경 변수 확인
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
```

#### **5. 메모리 부족 문제**
```dockerfile
# 문제: 배포 시 메모리 부족
# 해결: Docker 이미지 최적화
RUN pip install --no-cache-dir -r requirements.txt
```

### **디버깅 방법**

#### **로컬에서 배포 환경 테스트**
```bash
# 환경 변수 설정
export ENVIRONMENT=production
export PORT=8000
export HOST=0.0.0.0

# 애플리케이션 실행
python main.py
```

#### **로그 확인**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info(f"Environment: {ENVIRONMENT}")
logger.info(f"Host: {HOST}, Port: {PORT}")
```

---

## 🎯 배포 체크리스트

### **배포 전 체크리스트**
- [ ] 환경 변수가 모두 설정되었는지 확인
- [ ] CORS 설정이 배포 도메인을 포함하는지 확인
- [ ] 데이터베이스 연결이 정상인지 확인
- [ ] 헬스체크 엔드포인트가 작동하는지 확인
- [ ] 로그 레벨이 적절히 설정되었는지 확인

### **배포 후 체크리스트**
- [ ] 애플리케이션이 정상적으로 시작되는지 확인
- [ ] 모든 API 엔드포인트가 작동하는지 확인
- [ ] AI 기능이 정상 작동하는지 확인
- [ ] 데이터베이스 연결이 정상인지 확인
- [ ] SSL 인증서가 정상 발급되었는지 확인

---

## 📞 지원 및 문의

- **Issues**: [GitHub Issues](https://github.com/suhyoungjoon/bibe_coding_new/issues)
- **Discussions**: [GitHub Discussions](https://github.com/suhyoungjoon/bibe_coding_new/discussions)
- **이메일**: tjdudwns@gmnail.com

---

*이 문서는 바이브 코딩 프로젝트의 웹 배포를 위한 완전한 가이드입니다. 단계별로 따라하시면 성공적으로 웹 서비스를 배포할 수 있습니다.*
