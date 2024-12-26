from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging
import json
from ..core.llm import LLMClient

logger = logging.getLogger(__name__)

class AutoReplyAgent:
    """AI自动回复代理
    功能:
    1. 基于指令自动回复消息
    2. 维护多个活跃任务
    3. 支持任务时间管理
    4. 提供回复统计
    """
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        self._active_tasks: Dict[str, Any] = {}
        
    async def create_task(
        self,
        user_id: str,
        instruction: str,
        duration_hours: float = 2.0
    ) -> Dict[str, Any]:
        """创建新的自动回复任务"""
        
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=duration_hours)
        
        task = {
            "user_id": user_id,
            "instruction": instruction,
            "start_time": start_time,
            "end_time": end_time,
            "is_active": True,
            "total_replies": 0,
            "last_reply_at": None
        }
        
        self._active_tasks[user_id] = task
        return task
        
    async def handle_message(
        self,
        recipient_id: str,
        message_content: str,
        chat_history: List[Dict[str, Any]]
    ) -> Optional[str]:
        """处理收到的消息并生成回复"""
        
        task = self._active_tasks.get(recipient_id)
        if not task or not task["is_active"]:
            return None
            
        if datetime.now() > task["end_time"]:
            task["is_active"] = False
            return None
            
        prompt = f"""你正在帮助用户自动回复消息。

托管指令: {task['instruction']}

聊天记录:
{self._format_chat_history(chat_history)}

新消息: {message_content}

请根据托管指令和上下文生成合适的回复。只输出回复内容，不要有其他文字。
"""
        
        try:
            response = await self.llm.analyze(
                prompt=prompt,
                temperature=0.7
            )
            
            # 更新任务统计
            task["total_replies"] += 1
            task["last_reply_at"] = datetime.now()
            
            return response["content"]
            
        except Exception as e:
            logger.error(f"Generate reply failed: {str(e)}")
            return None
            
    def _format_chat_history(self, messages: List[Dict[str, Any]]) -> str:
        """格式化聊天历史"""
        return "\n".join([
            f"{msg['sender']}: {msg['content']}"
            for msg in messages[-10:]  # 只使用最近10条消息
        ])
