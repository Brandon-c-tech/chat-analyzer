from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
from .base import BaseAnalyzer

logger = logging.getLogger(__name__)

class ContactAnalyzer(BaseAnalyzer):
    """联系人分析器
    功能:
    1. 分析与联系人的对话历史
    2. 生成联系人画像
    3. 提取关键特征和标签
    4. 提供互动建议
    """
    
    async def analyze(
        self,
        messages: List[Dict[str, Any]],
        manual_note: Optional[str] = None,
        current_categories: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """分析联系人信息"""
        
        prompt = f"""分析以下与联系人的对话记录，生成联系人画像。
        请以JSON格式输出以下信息:
        
        1. profile: 联系人画像
           - personality: 性格特征
           - communication_style: 沟通风格
           - interests: 兴趣爱好
           - expertise: 专业领域
           
        2. relationship: 关系分析
           - interaction_frequency: 互动频率
           - relationship_type: 关系类型
           - key_topics: 主要讨论话题
           
        3. ai_note: AI生成的备注建议
        
        4. categories: 建议的分类标签
        
        5. interaction_suggestions: 互动建议
           - dos: 建议做的事
           - donts: 建议避免的事
           
        用户手动备注:
        {manual_note or "无"}
        
        当前分类标签:
        {', '.join(current_categories) if current_categories else "无"}
        
        对话记录:
        {self._format_messages(messages)}
        """
        
        try:
            result = await self.llm.analyze(prompt=prompt)
            
            # 添加元数据
            result["metadata"] = {
                "analyzed_at": datetime.now().isoformat(),
                "message_count": len(messages)
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Contact analysis failed: {str(e)}")
            raise
