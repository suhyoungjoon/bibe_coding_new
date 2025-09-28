"""
인덱스 관리 서비스
"""

import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from app.api.models import IndexStats
from app.core.config import settings
from app.core.exceptions import IndexBuildError
from app.ingest import rebuild_index
from app.vectorstore.faiss_store import FaissStore

logger = logging.getLogger(__name__)

class IndexService:
    """인덱스 관리 서비스"""
    
    def __init__(self):
        self.faiss_store = FaissStore()
    
    async def get_index_stats(self) -> IndexStats:
        """인덱스 통계 조회"""
        try:
            # 인덱스 파일 존재 확인
            index_path = settings.INDEX_DIR / "faiss.index"
            meta_path = settings.INDEX_DIR / "meta.json"
            
            if not index_path.exists() or not meta_path.exists():
                return IndexStats(
                    total_files=0,
                    total_chunks=0,
                    index_dimension=None,
                    last_built=None,
                    index_size_mb=None
                )
            
            # 인덱스 로드
            if not self.faiss_store.load():
                return IndexStats(
                    total_files=0,
                    total_chunks=0,
                    index_dimension=None,
                    last_built=None,
                    index_size_mb=None
                )
            
            # 파일 수 계산
            data_dir = Path(settings.DATA_DIR)
            total_files = len([f for f in data_dir.iterdir() if f.is_file()]) if data_dir.exists() else 0
            
            # 인덱스 크기 계산
            index_size_mb = index_path.stat().st_size / (1024 * 1024) if index_path.exists() else 0
            
            # 메타데이터 수정 시간
            last_built = datetime.fromtimestamp(meta_path.stat().st_mtime) if meta_path.exists() else None
            
            return IndexStats(
                total_files=total_files,
                total_chunks=len(self.faiss_store.meta),
                index_dimension=self.faiss_store.dim,
                last_built=last_built,
                index_size_mb=round(index_size_mb, 2)
            )
            
        except Exception as e:
            logger.error(f"인덱스 통계 조회 실패: {e}")
            raise IndexBuildError(
                message="인덱스 통계 조회 실패",
                details={"error": str(e)}
            )
    
    async def build_index(self, force_rebuild: bool = False) -> Dict[str, Any]:
        """인덱스 구축"""
        try:
            logger.info(f"인덱스 구축 시작 (force_rebuild: {force_rebuild})")
            
            # 데이터 디렉토리 확인
            data_dir = Path(settings.DATA_DIR)
            if not data_dir.exists():
                raise IndexBuildError(
                    message="데이터 디렉토리가 존재하지 않습니다",
                    details={"data_dir": str(data_dir)}
                )
            
            # 문서 파일 확인
            doc_files = [f for f in data_dir.iterdir() if f.is_file()]
            if not doc_files:
                raise IndexBuildError(
                    message="처리할 문서 파일이 없습니다",
                    details={"data_dir": str(data_dir)}
                )
            
            # 인덱스 구축
            files_processed, chunks_created = rebuild_index()
            
            if files_processed == 0:
                raise IndexBuildError(
                    message="인덱스 구축에 실패했습니다",
                    details={"files_processed": files_processed, "chunks_created": chunks_created}
                )
            
            logger.info(f"인덱스 구축 완료: {files_processed}개 파일, {chunks_created}개 청크")
            
            return {
                "files_processed": files_processed,
                "chunks_created": chunks_created,
                "timestamp": datetime.now()
            }
            
        except IndexBuildError:
            raise
        except Exception as e:
            logger.error(f"인덱스 구축 실패: {e}")
            raise IndexBuildError(
                message="인덱스 구축 중 오류가 발생했습니다",
                details={"error": str(e)}
            )
    
    async def delete_index(self) -> None:
        """인덱스 삭제"""
        try:
            logger.info("인덱스 삭제 시작")
            
            index_path = settings.INDEX_DIR / "faiss.index"
            meta_path = settings.INDEX_DIR / "meta.json"
            
            deleted_files = []
            
            if index_path.exists():
                index_path.unlink()
                deleted_files.append("faiss.index")
            
            if meta_path.exists():
                meta_path.unlink()
                deleted_files.append("meta.json")
            
            logger.info(f"인덱스 삭제 완료: {deleted_files}")
            
        except Exception as e:
            logger.error(f"인덱스 삭제 실패: {e}")
            raise IndexBuildError(
                message="인덱스 삭제 실패",
                details={"error": str(e)}
            )
    
    async def get_index_status(self) -> Dict[str, Any]:
        """인덱스 상태 조회"""
        try:
            index_path = settings.INDEX_DIR / "faiss.index"
            meta_path = settings.INDEX_DIR / "meta.json"
            
            status = {
                "index_exists": index_path.exists(),
                "meta_exists": meta_path.exists(),
                "data_dir_exists": Path(settings.DATA_DIR).exists(),
                "index_dir_exists": Path(settings.INDEX_DIR).exists(),
                "timestamp": datetime.now()
            }
            
            if status["index_exists"] and status["meta_exists"]:
                try:
                    if self.faiss_store.load():
                        status.update({
                            "index_loaded": True,
                            "meta_entries": len(self.faiss_store.meta),
                            "dimension": self.faiss_store.dim
                        })
                    else:
                        status["index_loaded"] = False
                except Exception as e:
                    status["index_loaded"] = False
                    status["load_error"] = str(e)
            else:
                status["index_loaded"] = False
            
            return status
            
        except Exception as e:
            logger.error(f"인덱스 상태 조회 실패: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now()
            }
    
    async def rebuild_index(self) -> Dict[str, Any]:
        """인덱스 재구축"""
        try:
            logger.info("인덱스 재구축 시작")
            
            # 기존 인덱스 삭제
            await self.delete_index()
            
            # 새 인덱스 구축
            result = await self.build_index(force_rebuild=True)
            
            logger.info("인덱스 재구축 완료")
            return result
            
        except Exception as e:
            logger.error(f"인덱스 재구축 실패: {e}")
            raise IndexBuildError(
                message="인덱스 재구축 실패",
                details={"error": str(e)}
            )
