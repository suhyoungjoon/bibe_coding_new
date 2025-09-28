"""
데이터 분석 유틸리티 모듈
통계 계산 및 데이터 처리 기능을 제공합니다.
"""

import statistics
from typing import List, Dict, Any
import json

class DataAnalyzer:
    """데이터 분석을 위한 클래스"""
    
    def __init__(self, data: List[float]):
        """
        데이터 분석기 초기화
        
        Args:
            data: 분석할 숫자 데이터 리스트
        """
        self.data = data
        self.results = {}
    
    def calculate_basic_stats(self) -> Dict[str, float]:
        """
        기본 통계 계산
        
        Returns:
            기본 통계 정보 딕셔너리
        """
        if not self.data:
            return {"error": "데이터가 없습니다."}
        
        stats = {
            "count": len(self.data),
            "mean": statistics.mean(self.data),
            "median": statistics.median(self.data),
            "mode": statistics.mode(self.data) if len(set(self.data)) < len(self.data) else "No mode",
            "min": min(self.data),
            "max": max(self.data),
            "range": max(self.data) - min(self.data)
        }
        
        # 표준편차 계산
        if len(self.data) > 1:
            stats["stdev"] = statistics.stdev(self.data)
            stats["variance"] = statistics.variance(self.data)
        
        self.results = stats
        return stats
    
    def find_outliers(self, threshold: float = 2.0) -> List[float]:
        """
        이상치 찾기 (Z-score 기반)
        
        Args:
            threshold: Z-score 임계값 (기본값: 2.0)
            
        Returns:
            이상치 리스트
        """
        if len(self.data) < 3:
            return []
        
        mean = statistics.mean(self.data)
        stdev = statistics.stdev(self.data)
        
        outliers = []
        for value in self.data:
            z_score = abs((value - mean) / stdev)
            if z_score > threshold:
                outliers.append(value)
        
        return outliers
    
    def generate_report(self) -> str:
        """
        분석 보고서 생성
        
        Returns:
            분석 보고서 문자열
        """
        if not self.results:
            self.calculate_basic_stats()
        
        report = f"""
=== 데이터 분석 보고서 ===
데이터 개수: {self.results.get('count', 0)}
평균: {self.results.get('mean', 0):.2f}
중앙값: {self.results.get('median', 0):.2f}
최솟값: {self.results.get('min', 0):.2f}
최댓값: {self.results.get('max', 0):.2f}
범위: {self.results.get('range', 0):.2f}
"""
        
        if 'stdev' in self.results:
            report += f"표준편차: {self.results['stdev']:.2f}\n"
            report += f"분산: {self.results['variance']:.2f}\n"
        
        outliers = self.find_outliers()
        if outliers:
            report += f"이상치: {outliers}\n"
        
        return report

def analyze_sales_data():
    """판매 데이터 분석 예제"""
    sales_data = [120, 150, 180, 200, 160, 140, 170, 190, 210, 130, 250, 110]
    
    analyzer = DataAnalyzer(sales_data)
    stats = analyzer.calculate_basic_stats()
    
    print("=== 판매 데이터 분석 ===")
    print(f"데이터: {sales_data}")
    print(analyzer.generate_report())
    
    return stats

def analyze_temperature_data():
    """온도 데이터 분석 예제"""
    temperature_data = [22.5, 23.1, 24.0, 25.2, 23.8, 22.9, 24.5, 26.1, 25.8, 24.2, 23.5, 25.0]
    
    analyzer = DataAnalyzer(temperature_data)
    stats = analyzer.calculate_basic_stats()
    
    print("=== 온도 데이터 분석 ===")
    print(f"데이터: {temperature_data}")
    print(analyzer.generate_report())
    
    return stats

if __name__ == "__main__":
    print("데이터 분석 모듈 테스트")
    print("=" * 50)
    
    # 판매 데이터 분석
    analyze_sales_data()
    print("\n" + "=" * 50)
    
    # 온도 데이터 분석
    analyze_temperature_data()

