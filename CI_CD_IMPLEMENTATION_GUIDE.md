# 🚀 바이브 코딩 프로젝트 CI/CD 구현 가이드

> **GitHub Actions를 활용한 자동화된 개발 파이프라인 구축**

## 📋 목차
- [개요](#개요)
- [단계별 구현 계획](#단계별-구현-계획)
- [Phase 1: 기본 CI 설정](#phase-1-기본-ci-설정)
- [Phase 2: Docker 통합](#phase-2-docker-통합)
- [Phase 3: 배포 자동화](#phase-3-배포-자동화)
- [웹 배포 가이드](#웹-배포-가이드)
- [배포 옵션 비교](#배포-옵션-비교)
- [구현 체크리스트](#구현-체크리스트)

## 🎯 개요

바이브 코딩 프로젝트의 CI/CD 파이프라인을 단계별로 구축하여 다음을 자동화합니다:
- 코드 테스트 실행
- 코드 품질 검사
- 보안 스캔
- Docker 이미지 빌드
- 자동 배포

## 📊 단계별 구현 계획

### **🔧 Phase 1: 기본 CI 설정 (즉시 구현 가능)**
- ✅ **1단계**: GitHub Actions 기본 워크플로우 설정
- ✅ **2단계**: 코드 품질 검사 자동화
- ✅ **3단계**: 보안 스캔 및 의존성 검사

### **🐳 Phase 2: Docker 통합 (중급)**
- ✅ **4단계**: Docker 이미지 빌드 자동화
- ✅ **5단계**: 컨테이너 레지스트리 연동

### **🚀 Phase 3: 배포 자동화 (고급)**
- ✅ **6단계**: 자동 배포 파이프라인
- ✅ **7단계**: 환경별 배포 설정

---

## 🔧 Phase 1: 기본 CI 설정

### **1단계: GitHub Actions 기본 워크플로우**

#### **파일 위치**: `.github/workflows/ci.yml`

```yaml
name: Continuous Integration

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run Azure OpenAI connection tests
      run: python test_azure_connection.py
      env:
        AZURE_OPENAI_API_KEY: ${{ secrets.AZURE_OPENAI_API_KEY }}
        AZURE_OPENAI_ENDPOINT: ${{ secrets.AZURE_OPENAI_ENDPOINT }}
    
    - name: Run code analysis tests
      run: python test_real_code_analysis.py
    
    - name: Run WebSocket tests
      run: python test_websocket_code_analysis.py
      continue-on-error: true  # WebSocket 테스트는 로컬 환경에서만 가능
    
    - name: Setup PostgreSQL tests
      run: python setup_postgresql.py
      continue-on-error: true  # PostgreSQL이 없는 환경에서는 스킵
```

### **2단계: 코드 품질 검사**

#### **파일 위치**: `.github/workflows/code-quality.yml`

```yaml
name: Code Quality

on: [push, pull_request]

jobs:
  lint-and-format:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install linting tools
      run: |
        python -m pip install --upgrade pip
        pip install black flake8 mypy isort pytest-cov
    
    - name: Run Black (code formatting)
      run: black --check --diff .
    
    - name: Run isort (import sorting)
      run: isort --check-only --diff .
    
    - name: Run flake8 (linting)
      run: flake8 .
    
    - name: Run mypy (type checking)
      run: mypy .
      continue-on-error: true  # 타입 체크는 점진적으로 적용
    
    - name: Generate coverage report
      run: |
        pytest --cov=app --cov-report=xml --cov-report=html
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
```

### **3단계: 보안 스캔**

#### **파일 위치**: `.github/workflows/security.yml`

```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
    
    - name: Run CodeQL Analysis
      uses: github/codeql-action/analyze@v2
      with:
        languages: python
    
    - name: Check for secrets
      uses: trufflesecurity/trufflehog@main
      with:
        path: ./
        base: main
        head: HEAD
        extra_args: --debug --only-verified
```

---

## 🐳 Phase 2: Docker 통합

### **4단계: Docker 이미지 빌드**

#### **파일 위치**: `.github/workflows/docker.yml`

```yaml
name: Docker Build

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: suhyoungjoon/bibe-coding
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=raw,value=latest,enable={{is_default_branch}}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

### **Dockerfile 생성**

#### **파일 위치**: `Dockerfile`

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

#### **파일 위치**: `.dockerignore`

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

## 🚀 Phase 3: 배포 자동화

### **5단계: 자동 배포**

#### **파일 위치**: `.github/workflows/deploy.yml`

```yaml
name: Deploy

on:
  push:
    branches: [ main ]
  release:
    types: [ published ]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    needs: [test, lint-and-format, security]
    if: github.ref == 'refs/heads/main'
    environment: staging
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Deploy to Railway Staging
      run: |
        echo "🚀 Deploying to staging environment..."
        # Railway CLI를 통한 배포
        # railway login --token ${{ secrets.RAILWAY_TOKEN }}
        # railway up --service staging
    
    - name: Run smoke tests
      run: |
        echo "🧪 Running smoke tests..."
        # 배포 후 기본 기능 테스트

  deploy-production:
    runs-on: ubuntu-latest
    needs: [test, lint-and-format, security]
    if: startsWith(github.ref, 'refs/tags/v')
    environment: production
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Deploy to Railway Production
      run: |
        echo "🚀 Deploying to production environment..."
        # Railway CLI를 통한 프로덕션 배포
    
    - name: Run production tests
      run: |
        echo "🧪 Running production tests..."
        # 프로덕션 환경에서 전체 테스트 실행
    
    - name: Notify deployment success
      uses: 8398a7/action-slack@v3
      with:
        status: success
        text: 'Production deployment successful! 🎉'
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### **6단계: 환경별 배포 설정**

#### **파일 위치**: `.github/workflows/environment-deploy.yml`

```yaml
name: Environment Deployment

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        default: 'staging'
        type: choice
        options:
        - staging
        - production

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.environment }}
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set environment variables
      run: |
        echo "ENVIRONMENT=${{ github.event.inputs.environment }}" >> $GITHUB_ENV
        echo "DEPLOY_URL=${{ secrets.DEPLOY_URL_${{ github.event.inputs.environment }} }}" >> $GITHUB_ENV
    
    - name: Deploy to ${{ github.event.inputs.environment }}
      run: |
        echo "🚀 Deploying to ${{ github.event.inputs.environment }}..."
        # 환경별 배포 스크립트 실행
    
    - name: Verify deployment
      run: |
        echo "✅ Verifying ${{ github.event.inputs.environment }} deployment..."
        # 배포 검증 테스트
```

---

## 🌐 웹 배포 가이드

### **배포 옵션 비교**

| 방법 | 난이도 | 비용 | 성능 | 관리 편의성 | 추천도 |
|------|--------|------|------|-------------|--------|
| **Railway** | ⭐⭐ | $5/월 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Render** | ⭐⭐ | 무료~$7/월 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Heroku** | ⭐⭐ | $7/월 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **AWS EC2** | ⭐⭐⭐⭐ | $10-50/월 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **Google Cloud** | ⭐⭐⭐⭐ | $10-50/월 | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **DigitalOcean** | ⭐⭐⭐ | $6/월 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

### **Railway 배포 설정**

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
    "healthcheckTimeout": 300
  }
}
```

#### **환경 변수 설정**
```env
# Railway에서 설정할 환경 변수들
AZURE_OPENAI_API_KEY=your_actual_key
AZURE_OPENAI_ENDPOINT=https://openai-syj.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-06-01
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
ENVIRONMENT=production
PORT=8000
```

### **배포 전 코드 수정사항**

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
    HOST: str = "0.0.0.0" if ENVIRONMENT == "production" else "127.0.0.1"
    
    # CORS 설정
    ALLOWED_ORIGINS: list = [
        "https://*.railway.app",
        "https://bibe-coding.railway.app",
        "http://localhost:3000",
        "http://localhost:8000"
    ] if ENVIRONMENT == "production" else ["*"]
    
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
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## ✅ 구현 체크리스트

### **Phase 1: 기본 CI 설정**
- [ ] `.github/workflows/ci.yml` 생성
- [ ] `.github/workflows/code-quality.yml` 생성
- [ ] `.github/workflows/security.yml` 생성
- [ ] GitHub Secrets 설정:
  - [ ] `AZURE_OPENAI_API_KEY`
  - [ ] `AZURE_OPENAI_ENDPOINT`
  - [ ] `DOCKER_USERNAME`
  - [ ] `DOCKER_PASSWORD`

### **Phase 2: Docker 통합**
- [ ] `Dockerfile` 생성
- [ ] `.dockerignore` 생성
- [ ] `.github/workflows/docker.yml` 생성
- [ ] Docker Hub 계정 연결

### **Phase 3: 배포 자동화**
- [ ] `.github/workflows/deploy.yml` 생성
- [ ] `.github/workflows/environment-deploy.yml` 생성
- [ ] Railway 계정 생성 및 연결
- [ ] 환경별 Secrets 설정

### **배포 준비**
- [ ] `railway.json` 생성
- [ ] 환경 변수 설정 파일 수정
- [ ] CORS 설정 업데이트
- [ ] 헬스체크 엔드포인트 확인

---

## 🎯 우선순위별 구현 순서

### **🔥 즉시 구현 (High Priority)**
1. **기본 CI 워크플로우** - 테스트 자동화
2. **코드 품질 검사** - Black, flake8, mypy
3. **보안 스캔** - 의존성 취약점 검사

### **📈 단기 목표 (Medium Priority)**
4. **Docker 이미지 빌드** - 컨테이너화
5. **자동 배포** - 스테이징 환경

### **🚀 장기 목표 (Low Priority)**
6. **다중 환경 배포** - dev/staging/prod
7. **모니터링 및 알림** - Slack/Discord 연동

---

## 💡 다음 단계

1. **지금**: GitHub Actions 워크플로우 파일들 생성
2. **다음**: GitHub Secrets 설정 및 테스트
3. **그 다음**: Railway 배포 테스트
4. **최종**: 프로덕션 배포 및 모니터링 설정

---

## 📞 지원 및 문의

- **Issues**: [GitHub Issues](https://github.com/suhyoungjoon/bibe_coding_new/issues)
- **Discussions**: [GitHub Discussions](https://github.com/suhyoungjoon/bibe_coding_new/discussions)
- **이메일**: tjdudwns@gmnail.com

---

*이 문서는 바이브 코딩 프로젝트의 CI/CD 구현을 위한 완전한 가이드입니다. 단계별로 따라하시면 자동화된 개발 파이프라인을 구축할 수 있습니다.*
