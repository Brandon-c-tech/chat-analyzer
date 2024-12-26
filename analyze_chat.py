import asyncio
import json
from chat_analyzer.core.llm import LLMClient
from chat_analyzer.analyzers.conversation import ConversationAnalyzer

async def main():
    # 初始化 LLM 客户端
    llm = LLMClient(
        openai_api_key="your-openai-key",
        anthropic_api_key="your-anthropic-key"
    )
    
    # 创建分析器
    analyzer = ConversationAnalyzer(llm)
    
    # 示例消息
    messages = [
        {"sender": "用户A", "content": "我们来讨论一下项目进度"},
        {"sender": "用户B", "content": "好的,前端已经完成了80%"},
        {"sender": "用户A", "content": "那后端开发情况如何?"}
    ]
    
    # 分析会话
    result = await analyzer.analyze(messages)
    print("\n会话分析结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 实时分析新消息
    new_message = {
        "sender": "用户B",
        "content": "后端还需要两周时间完成核心功能"
    }
    
    updated = await analyzer.analyze_realtime(new_message, result)
    print("\n更新后的分析:")
    print(json.dumps(updated, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
