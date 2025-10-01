#!/usr/bin/env python3
"""
Railway에서 FastAPI와 Streamlit을 동시에 실행하는 스크립트
"""
import subprocess
import threading
import time
import os
import signal
import sys
from pathlib import Path

def run_fastapi():
    """FastAPI 서버 실행"""
    print("🚀 FastAPI 서버 시작...")
    subprocess.run([
        "python", "main.py"
    ])

def run_streamlit():
    """Streamlit 서버 실행"""
    print("🖥️ Streamlit 서버 시작...")
    # Streamlit이 시작되기 전에 잠시 대기
    time.sleep(5)
    subprocess.run([
        "streamlit", "run", "ui/streamlit_app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--server.headless=true",
        "--server.enableCORS=false",
        "--server.enableXsrfProtection=false"
    ])

def signal_handler(sig, frame):
    """시그널 핸들러"""
    print("\n🛑 서버 종료 중...")
    sys.exit(0)

if __name__ == "__main__":
    # 시그널 핸들러 등록
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🚀 Agentic AI 서버 시작 (FastAPI + Streamlit)")
    print(f"📍 PORT: {os.getenv('PORT', '8000')}")
    print(f"📍 STREAMLIT_PORT: 8501")
    
    # FastAPI와 Streamlit을 별도 스레드에서 실행
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    streamlit_thread = threading.Thread(target=run_streamlit, daemon=True)
    
    fastapi_thread.start()
    streamlit_thread.start()
    
    try:
        # 메인 스레드에서 대기
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 서버 종료 중...")
        sys.exit(0)
