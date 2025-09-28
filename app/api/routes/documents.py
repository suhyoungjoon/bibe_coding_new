"""
문서 관리 라우트
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pathlib import Path
import shutil
import logging
from datetime import datetime
from typing import List

from app.api.models import DocumentInfo, ErrorResponse
from app.core.config import settings
from app.core.exceptions import DocumentNotFoundError

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/documents", response_model=List[DocumentInfo])
async def list_documents():
    """문서 목록 조회"""
    try:
        documents = []
        data_dir = Path(settings.DATA_DIR)
        
        if not data_dir.exists():
            return []
        
        for file_path in data_dir.iterdir():
            if file_path.is_file():
                try:
                    stat = file_path.stat()
                    documents.append(DocumentInfo(
                        name=file_path.name,
                        path=str(file_path),
                        size=stat.st_size,
                        modified_time=datetime.fromtimestamp(stat.st_mtime),
                        file_type=file_path.suffix.lower()
                    ))
                except Exception as e:
                    logger.warning(f"파일 정보 읽기 실패: {file_path.name} - {e}")
                    continue
        
        # 수정 시간 기준으로 정렬
        documents.sort(key=lambda x: x.modified_time, reverse=True)
        
        logger.info(f"문서 목록 조회: {len(documents)}개 파일")
        return documents
        
    except Exception as e:
        logger.error(f"문서 목록 조회 실패: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"문서 목록 조회 실패: {str(e)}"
        )

@router.post("/documents/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """문서 업로드"""
    try:
        uploaded_files = []
        data_dir = Path(settings.DATA_DIR)
        data_dir.mkdir(parents=True, exist_ok=True)
        
        for file in files:
            # 파일 저장
            file_path = data_dir / file.filename
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            uploaded_files.append({
                "filename": file.filename,
                "size": file_path.stat().st_size,
                "path": str(file_path)
            })
            
            logger.info(f"파일 업로드 완료: {file.filename}")
        
        return {
            "message": f"{len(uploaded_files)}개 파일이 성공적으로 업로드되었습니다.",
            "uploaded_files": uploaded_files
        }
        
    except Exception as e:
        logger.error(f"파일 업로드 실패: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"파일 업로드 실패: {str(e)}"
        )

@router.get("/documents/{filename}")
async def download_document(filename: str):
    """문서 다운로드"""
    try:
        file_path = Path(settings.DATA_DIR) / filename
        
        if not file_path.exists():
            raise DocumentNotFoundError(
                message=f"파일을 찾을 수 없습니다: {filename}",
                details={"filename": filename}
            )
        
        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type='application/octet-stream'
        )
        
    except DocumentNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail={
                "error": e.error_type,
                "message": e.message,
                "details": e.details
            }
        )
    except Exception as e:
        logger.error(f"파일 다운로드 실패: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"파일 다운로드 실패: {str(e)}"
        )

@router.delete("/documents/{filename}")
async def delete_document(filename: str):
    """문서 삭제"""
    try:
        file_path = Path(settings.DATA_DIR) / filename
        
        if not file_path.exists():
            raise DocumentNotFoundError(
                message=f"파일을 찾을 수 없습니다: {filename}",
                details={"filename": filename}
            )
        
        file_path.unlink()
        
        logger.info(f"파일 삭제 완료: {filename}")
        return {
            "message": f"파일이 성공적으로 삭제되었습니다: {filename}",
            "filename": filename
        }
        
    except DocumentNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail={
                "error": e.error_type,
                "message": e.message,
                "details": e.details
            }
        )
    except Exception as e:
        logger.error(f"파일 삭제 실패: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"파일 삭제 실패: {str(e)}"
        )

@router.get("/documents/{filename}/content")
async def get_document_content(filename: str, max_length: int = 1000):
    """문서 내용 조회"""
    try:
        file_path = Path(settings.DATA_DIR) / filename
        
        if not file_path.exists():
            raise DocumentNotFoundError(
                message=f"파일을 찾을 수 없습니다: {filename}",
                details={"filename": filename}
            )
        
        # 텍스트 파일 읽기
        try:
            content = file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            content = file_path.read_text(encoding='cp949')
        
        # 길이 제한
        if len(content) > max_length:
            content = content[:max_length] + "..."
        
        return {
            "filename": filename,
            "content": content,
            "length": len(content),
            "truncated": len(content) > max_length
        }
        
    except DocumentNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail={
                "error": e.error_type,
                "message": e.message,
                "details": e.details
            }
        )
    except Exception as e:
        logger.error(f"문서 내용 조회 실패: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"문서 내용 조회 실패: {str(e)}"
        )
