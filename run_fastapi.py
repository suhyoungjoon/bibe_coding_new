#!/usr/bin/env python3
"""
FastAPI 서버 실행 스크립트
"""

import uvicorn
import sys
import os
from pathlib import Path

def main():
    """FastAPI 서버 실행"""
    print("🚀 Agentic AI FastAPI 서버 시작")
    print("=" * 50)
    
    # 현재 디렉토리를 Python 경로에 추가
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    # 환경 변수 설정
    os.environ.setdefault("PYTHONPATH", str(current_dir))
    
    try:
        # FastAPI 서버 실행
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n🛑 서버가 중지되었습니다.")
    except Exception as e:
        print(f"❌ 서버 실행 실패: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
