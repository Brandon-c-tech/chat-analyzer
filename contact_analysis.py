import asyncio
from chat_analyzer.core.llm import LLMClient
from chat_analyzer.analyzers.contact import ContactAnalyzer
from chat_analyzer.agents.auto_reply import AutoReplyAgent

async def main():
    # 初始化 LLM 客户端
    llm = LLMClient(openai_api_key="your-key")
    
    # 创建联系人分析器
    contact_analyzer = ContactAnalyzer(llm)
    
    # 示例消息
    messages = [
        {"sender": "contact", "content": "我们讨论一下新项目的技术方案"},
        {"sender": "user", "content": "好的,你觉得用Python怎么样?"},
        {"sender": "contact", "content": "Python很适合,我之前做过类似项目"}
    ]
    
    # 分析联系人
    result = await contact_analyzer.analyze(
        messages=messages,
        manual_note="技术同事",
        current_categories=["工作", "技术"]
    )
    
    print("\n联系人分析结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 创建自动回复代理
    auto_reply = AutoReplyAgent(llm)
    
    # 创建托管任务
    task = await auto_reply.create_task(
        user_id="user123",
        instruction="我在开会,帮我回复技术相关的问题,态度友好专业",
        duration_hours=2.0
    )
    
    # 测试自动回复
    new_message = "这个项目用什么框架比较好?"
    reply = await auto_reply.handle_message(
        recipient_id="user123",
        message_content=new_message,
        chat_history=messages
    )
    
    print("\n自动回复:")
    print(reply)

if __name__ == "__main__":
    asyncio.run(main())
