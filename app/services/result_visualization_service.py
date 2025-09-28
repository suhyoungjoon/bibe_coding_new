"""
실행 결과 시각화 서비스
실행 결과를 차트, 그래프, 표 등으로 시각화
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import re

logger = logging.getLogger(__name__)

class ResultVisualizationService:
    """실행 결과 시각화 서비스"""
    
    def __init__(self):
        self.visualization_types = {
            "chart": self._create_chart_visualization,
            "table": self._create_table_visualization,
            "graph": self._create_graph_visualization,
            "timeline": self._create_timeline_visualization,
            "metrics": self._create_metrics_visualization,
        }
    
    async def visualize_result(
        self, 
        result_data: Dict[str, Any], 
        visualization_type: str = "auto"
    ) -> Dict[str, Any]:
        """실행 결과 시각화"""
        try:
            if visualization_type == "auto":
                visualization_type = self._detect_visualization_type(result_data)
            
            if visualization_type not in self.visualization_types:
                return self._create_default_visualization(result_data)
            
            visualizer = self.visualization_types[visualization_type]
            return await visualizer(result_data)
            
        except Exception as e:
            logger.error(f"시각화 생성 실패: {str(e)}")
            return self._create_default_visualization(result_data)
    
    def _detect_visualization_type(self, result_data: Dict[str, Any]) -> str:
        """결과 데이터를 분석하여 적절한 시각화 타입 결정"""
        output = result_data.get("output", "")
        
        # 숫자 데이터가 많으면 차트
        if self._has_numeric_data(output):
            return "chart"
        
        # 테이블 형태의 데이터면 테이블
        if self._has_table_data(output):
            return "table"
        
        # 실행 시간이나 메트릭 데이터면 메트릭
        if result_data.get("execution_time") or result_data.get("memory_used"):
            return "metrics"
        
        # 기본값
        return "default"
    
    def _has_numeric_data(self, output: str) -> bool:
        """숫자 데이터가 포함되어 있는지 확인"""
        # 숫자 패턴 검사
        numeric_patterns = [
            r'\d+\.\d+',  # 소수점 숫자
            r'\d+',       # 정수
            r'\[[\d\.,\s]+\]',  # 배열 형태
            r'\{[\d\.,\s:]+\}',  # 딕셔너리 형태
        ]
        
        for pattern in numeric_patterns:
            if re.search(pattern, output):
                return True
        return False
    
    def _has_table_data(self, output: str) -> bool:
        """테이블 형태의 데이터가 있는지 확인"""
        lines = output.strip().split('\n')
        if len(lines) < 2:
            return False
        
        # 첫 번째 줄에 구분자가 있는지 확인
        first_line = lines[0]
        separators = ['|', '\t', ',', ';']
        
        for sep in separators:
            if sep in first_line and len(first_line.split(sep)) > 1:
                return True
        
        return False
    
    async def _create_chart_visualization(self, result_data: Dict[str, Any]) -> Dict[str, Any]:
        """차트 시각화 생성"""
        output = result_data.get("output", "")
        
        # 데이터 파싱
        chart_data = self._parse_chart_data(output)
        
        return {
            "type": "chart",
            "title": "실행 결과 차트",
            "data": chart_data,
            "config": {
                "type": "line",  # line, bar, pie 등
                "responsive": True,
                "plugins": {
                    "legend": {
                        "position": "top"
                    }
                }
            },
            "html": self._generate_chart_html(chart_data)
        }
    
    async def _create_table_visualization(self, result_data: Dict[str, Any]) -> Dict[str, Any]:
        """테이블 시각화 생성"""
        output = result_data.get("output", "")
        
        # 테이블 데이터 파싱
        table_data = self._parse_table_data(output)
        
        return {
            "type": "table",
            "title": "실행 결과 테이블",
            "data": table_data,
            "html": self._generate_table_html(table_data)
        }
    
    async def _create_graph_visualization(self, result_data: Dict[str, Any]) -> Dict[str, Any]:
        """그래프 시각화 생성"""
        output = result_data.get("output", "")
        
        # 그래프 데이터 파싱
        graph_data = self._parse_graph_data(output)
        
        return {
            "type": "graph",
            "title": "실행 결과 그래프",
            "data": graph_data,
            "html": self._generate_graph_html(graph_data)
        }
    
    async def _create_timeline_visualization(self, result_data: Dict[str, Any]) -> Dict[str, Any]:
        """타임라인 시각화 생성"""
        execution_time = result_data.get("execution_time", 0)
        memory_usage = result_data.get("memory_used", 0)
        cpu_usage = result_data.get("cpu_usage", 0)
        
        timeline_data = [
            {
                "timestamp": datetime.now().isoformat(),
                "event": "실행 시작",
                "duration": 0,
                "memory": 0,
                "cpu": 0
            },
            {
                "timestamp": (datetime.now() + timedelta(milliseconds=execution_time)).isoformat(),
                "event": "실행 완료",
                "duration": execution_time,
                "memory": memory_usage,
                "cpu": cpu_usage
            }
        ]
        
        return {
            "type": "timeline",
            "title": "실행 타임라인",
            "data": timeline_data,
            "html": self._generate_timeline_html(timeline_data)
        }
    
    async def _create_metrics_visualization(self, result_data: Dict[str, Any]) -> Dict[str, Any]:
        """메트릭 시각화 생성"""
        metrics = {
            "execution_time": result_data.get("execution_time", 0),
            "memory_used": result_data.get("memory_used", 0),
            "cpu_usage": result_data.get("cpu_usage", 0),
            "success": result_data.get("success", False),
            "output_length": len(result_data.get("output", "")),
            "error_count": len(result_data.get("error", "").split('\n')) if result_data.get("error") else 0
        }
        
        return {
            "type": "metrics",
            "title": "실행 메트릭",
            "data": metrics,
            "html": self._generate_metrics_html(metrics)
        }
    
    def _create_default_visualization(self, result_data: Dict[str, Any]) -> Dict[str, Any]:
        """기본 시각화 생성"""
        return {
            "type": "default",
            "title": "실행 결과",
            "data": result_data,
            "html": self._generate_default_html(result_data)
        }
    
    def _parse_chart_data(self, output: str) -> List[Dict[str, Any]]:
        """차트 데이터 파싱"""
        data = []
        lines = output.strip().split('\n')
        
        for i, line in enumerate(lines):
            # 숫자 데이터 추출
            numbers = re.findall(r'-?\d+\.?\d*', line)
            if numbers:
                for j, num in enumerate(numbers):
                    try:
                        value = float(num)
                        data.append({
                            "x": i,
                            "y": value,
                            "series": f"Series {j + 1}"
                        })
                    except ValueError:
                        continue
        
        return data
    
    def _parse_table_data(self, output: str) -> Dict[str, Any]:
        """테이블 데이터 파싱"""
        lines = output.strip().split('\n')
        
        if not lines:
            return {"headers": [], "rows": []}
        
        # 헤더 추출 (첫 번째 줄)
        headers = []
        first_line = lines[0]
        
        # 구분자 찾기
        separators = ['|', '\t', ',', ';']
        separator = None
        
        for sep in separators:
            if sep in first_line:
                separator = sep
                break
        
        if separator:
            headers = [h.strip() for h in first_line.split(separator)]
        else:
            headers = [f"Column {i+1}" for i in range(len(first_line.split()))]
        
        # 데이터 행 파싱
        rows = []
        for line in lines[1:]:
            if separator:
                row = [cell.strip() for cell in line.split(separator)]
            else:
                row = line.split()
            
            if len(row) == len(headers):
                rows.append(row)
        
        return {
            "headers": headers,
            "rows": rows
        }
    
    def _parse_graph_data(self, output: str) -> Dict[str, Any]:
        """그래프 데이터 파싱"""
        # 간단한 그래프 데이터 파싱 (실제로는 더 복잡할 수 있음)
        nodes = []
        edges = []
        
        lines = output.strip().split('\n')
        for line in lines:
            # 노드 패턴 찾기 (예: "A -> B")
            edge_match = re.search(r'(\w+)\s*->\s*(\w+)', line)
            if edge_match:
                source, target = edge_match.groups()
                if source not in nodes:
                    nodes.append(source)
                if target not in nodes:
                    nodes.append(target)
                edges.append({"source": source, "target": target})
        
        return {
            "nodes": [{"id": node, "label": node} for node in nodes],
            "edges": edges
        }
    
    def _generate_chart_html(self, chart_data: List[Dict[str, Any]]) -> str:
        """차트 HTML 생성"""
        if not chart_data:
            return "<div class='no-data'>표시할 차트 데이터가 없습니다.</div>"
        
        # Chart.js를 사용한 간단한 차트 HTML
        data_json = json.dumps(chart_data)
        
        return f"""
        <div class="chart-container">
            <canvas id="resultChart" width="400" height="200"></canvas>
        </div>
        <script>
            const ctx = document.getElementById('resultChart').getContext('2d');
            const chartData = {data_json};
            
            new Chart(ctx, {{
                type: 'line',
                data: {{
                    datasets: [{{
                        label: '실행 결과',
                        data: chartData,
                        borderColor: 'rgb(102, 126, 234)',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        tension: 0.1
                    }}]
                }},
                options: {{
                    responsive: true,
                    scales: {{
                        x: {{
                            type: 'linear',
                            position: 'bottom'
                        }}
                    }}
                }}
            }});
        </script>
        """
    
    def _generate_table_html(self, table_data: Dict[str, Any]) -> str:
        """테이블 HTML 생성"""
        headers = table_data.get("headers", [])
        rows = table_data.get("rows", [])
        
        if not headers and not rows:
            return "<div class='no-data'>표시할 테이블 데이터가 없습니다.</div>"
        
        html = "<table class='result-table'>"
        
        # 헤더
        if headers:
            html += "<thead><tr>"
            for header in headers:
                html += f"<th>{header}</th>"
            html += "</tr></thead>"
        
        # 데이터 행
        if rows:
            html += "<tbody>"
            for row in rows:
                html += "<tr>"
                for cell in row:
                    html += f"<td>{cell}</td>"
                html += "</tr>"
            html += "</tbody>"
        
        html += "</table>"
        
        return html
    
    def _generate_graph_html(self, graph_data: Dict[str, Any]) -> str:
        """그래프 HTML 생성"""
        nodes = graph_data.get("nodes", [])
        edges = graph_data.get("edges", [])
        
        if not nodes:
            return "<div class='no-data'>표시할 그래프 데이터가 없습니다.</div>"
        
        # 간단한 SVG 그래프 생성
        html = f"""
        <div class="graph-container">
            <svg width="400" height="300" viewBox="0 0 400 300">
                <defs>
                    <marker id="arrowhead" markerWidth="10" markerHeight="7" 
                            refX="9" refY="3.5" orient="auto">
                        <polygon points="0 0, 10 3.5, 0 7" fill="#667eea" />
                    </marker>
                </defs>
        """
        
        # 노드 그리기
        for i, node in enumerate(nodes):
            x = 50 + (i % 4) * 80
            y = 50 + (i // 4) * 80
            html += f"""
                <circle cx="{x}" cy="{y}" r="20" fill="#667eea" />
                <text x="{x}" y="{y + 5}" text-anchor="middle" fill="white" font-size="12">
                    {node['label']}
                </text>
            """
        
        # 엣지 그리기
        for edge in edges:
            # 간단한 선 그리기 (실제로는 더 복잡한 계산 필요)
            html += f"""
                <line x1="70" y1="50" x2="130" y2="50" 
                      stroke="#667eea" stroke-width="2" 
                      marker-end="url(#arrowhead)" />
            """
        
        html += """
            </svg>
        </div>
        """
        
        return html
    
    def _generate_timeline_html(self, timeline_data: List[Dict[str, Any]]) -> str:
        """타임라인 HTML 생성"""
        html = "<div class='timeline-container'>"
        
        for i, event in enumerate(timeline_data):
            html += f"""
                <div class="timeline-item">
                    <div class="timeline-marker"></div>
                    <div class="timeline-content">
                        <h4>{event['event']}</h4>
                        <p>시간: {event['timestamp']}</p>
                        <p>지속시간: {event['duration']}ms</p>
                        <p>메모리: {event['memory']}MB</p>
                        <p>CPU: {event['cpu']}%</p>
                    </div>
                </div>
            """
        
        html += "</div>"
        
        return html
    
    def _generate_metrics_html(self, metrics: Dict[str, Any]) -> str:
        """메트릭 HTML 생성"""
        html = "<div class='metrics-container'>"
        
        for key, value in metrics.items():
            if key == "success":
                icon = "✅" if value else "❌"
                display_value = "성공" if value else "실패"
            elif key == "execution_time":
                icon = "⏱️"
                display_value = f"{value}ms"
            elif key == "memory_used":
                icon = "💾"
                display_value = f"{value}MB"
            elif key == "cpu_usage":
                icon = "🖥️"
                display_value = f"{value}%"
            elif key == "output_length":
                icon = "📄"
                display_value = f"{value}자"
            elif key == "error_count":
                icon = "⚠️"
                display_value = f"{value}개"
            else:
                icon = "📊"
                display_value = str(value)
            
            html += f"""
                <div class="metric-item">
                    <span class="metric-icon">{icon}</span>
                    <span class="metric-label">{self._format_metric_label(key)}</span>
                    <span class="metric-value">{display_value}</span>
                </div>
            """
        
        html += "</div>"
        
        return html
    
    def _generate_default_html(self, result_data: Dict[str, Any]) -> str:
        """기본 HTML 생성"""
        output = result_data.get("output", "")
        error = result_data.get("error", "")
        
        html = "<div class='default-result'>"
        
        if output:
            html += f"<div class='output'><pre>{output}</pre></div>"
        
        if error:
            html += f"<div class='error'><pre>{error}</pre></div>"
        
        html += "</div>"
        
        return html
    
    def _format_metric_label(self, key: str) -> str:
        """메트릭 라벨 포맷팅"""
        labels = {
            "execution_time": "실행 시간",
            "memory_used": "메모리 사용량",
            "cpu_usage": "CPU 사용률",
            "success": "실행 상태",
            "output_length": "출력 길이",
            "error_count": "오류 개수"
        }
        return labels.get(key, key.replace("_", " ").title())
