from typing import Dict, Any, List
import logging
from .base import BaseAnalyzer

logger = logging.getLogger(__name__)

class ConversationAnalyzer(BaseAnalyzer):
    """会话分析器
    分析对话内容,提取主题、关键词等信息
    """
    
    async def analyze(
        self,
        messages: List[Dict[str, Any]],
        save_result: bool = True
    ) -> Dict[str, Any]:
        """分析整个会话"""
        
        # 构建分析提示词
        prompt = f"""分析以下对话内容,提取关键信息并以JSON格式输出:
        1. topics: 讨论的主要话题列表
        2. keywords: 重要关键词列表
        3. summary: 对话的简要总结
        4. participants: 参与者及其主要观点
        5. next_actions: 建议的后续行动

        对话内容:
        {self._format_messages(messages)}
        """
        
        try:
            # 调用 LLM 分析
            result = await self.llm.analyze(prompt=prompt)
            
            # 添加元数据
            result["metadata"] = {
                "analyzed_at": datetime.now().isoformat(),
                "message_count": len(messages)
            }
            
            # 保存结果
            if save_result:
                self._save_analysis("conversation", result)
                
            return result
            
        except Exception as e:
            logger.error(f"Conversation analysis failed: {str(e)}")
            raise
            
    async def analyze_realtime(
        self,
        new_message: Dict[str, Any],
        previous_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """实时分析新消息的影响"""
        
        prompt = f"""基于之前的分析结果和新消息,更新会话分析。
        只输出需要更新的内容。
        
        之前的分析:
        {json.dumps(previous_analysis, ensure_ascii=False, indent=2)}
        
        新消息:
        {new_message['sender']}: {new_message['content']}
        """
        
        try:
            updates = await self.llm.analyze(prompt=prompt)
            
            # 合并更新
            result = previous_analysis.copy()
            self._deep_update(result, updates)
            
            return result
            
        except Exception as e:
            logger.error(f"Realtime analysis failed: {str(e)}")
            raise
