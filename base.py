from typing import Dict, Any, List
import json
import logging
from datetime import datetime
from ..core.llm import LLMClient

logger = logging.getLogger(__name__)

class BaseAnalyzer:
    """基础分析器"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        
    def _save_analysis(self, analysis_id: str, result: Dict[str, Any]):
        """保存分析结果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_{analysis_id}_{timestamp}.json"
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        logger.info(f"Analysis result saved to {filename}")
        
    def _format_messages(self, messages: List[Dict[str, Any]]) -> str:
        """格式化消息记录"""
        return "\n".join([
            f"{msg['sender']}: {msg['content']}"
            for msg in messages
        ])
