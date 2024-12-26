# ChatAnalyzer

A powerful toolkit for analyzing chat conversations using LLMs (Large Language Models). Extract topics, sentiments, and insights from your chat data with ease.

## Features

- 🤖 Multi-LLM support (OpenAI GPT-4, Anthropic Claude)
- 📊 Comprehensive conversation analysis
- ⚡ Real-time message analysis
- 💾 Incremental result saving
- 🔄 Automatic retry mechanism
- 📝 Detailed logging

## Installation

Install from PyPI:

```bash
pip install chat-analyzer
```

Or install from source:

```bash
git clone https://github.com/yourusername/chat-analyzer.git
cd chat-analyzer
pip install -e .
```

## Quick Start

Here's a simple example of analyzing a conversation:

```python
import asyncio
from chat_analyzer.core.llm import LLMClient
from chat_analyzer.analyzers.conversation import ConversationAnalyzer

async def main():
    # Initialize LLM client
    llm = LLMClient(
        openai_api_key="your-openai-key",
        anthropic_api_key="your-anthropic-key"
    )
    
    # Create analyzer
    analyzer = ConversationAnalyzer(llm)
    
    # Sample messages
    messages = [
        {"sender": "Alice", "content": "Let's discuss the project timeline"},
        {"sender": "Bob", "content": "Sure, frontend is 80% complete"},
        {"sender": "Alice", "content": "How about the backend progress?"}
    ]
    
    # Analyze conversation
    result = await analyzer.analyze(messages)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## Analysis Output

The analyzer returns structured JSON data containing:

```json
{
    "topics": ["project timeline", "development progress"],
    "keywords": ["frontend", "backend", "progress"],
    "summary": "Discussion about project progress with focus on frontend completion",
    "participants": {
        "Alice": "Project manager inquiring about progress",
        "Bob": "Developer reporting on frontend status"
    },
    "next_actions": [
        "Get backend progress update",
        "Set timeline for remaining tasks"
    ],
    "metadata": {
        "analyzed_at": "2024-03-21T10:30:00Z",
        "message_count": 3
    }
}
```

## Advanced Usage

### Real-time Analysis

Analyze new messages as they arrive:

```python
# Initial analysis
result = await analyzer.analyze(messages)

# New message arrives
new_message = {
    "sender": "Bob",
    "content": "Backend needs two more weeks for core features"
}

# Update analysis
updated_result = await analyzer.analyze_realtime(new_message, result)
```

### Custom Analysis

Create your own analyzer by extending the BaseAnalyzer:

```python
from chat_analyzer.analyzers.base import BaseAnalyzer

class CustomAnalyzer(BaseAnalyzer):
    async def analyze(self, messages, **kwargs):
        # Your custom analysis logic here
        prompt = self._build_custom_prompt(messages)
        return await self.llm.analyze(prompt=prompt, **kwargs)
```

## Configuration

Configure the LLM client with your API keys:

```python
from chat_analyzer.core.llm import LLMClient

llm = LLMClient(
    openai_api_key="your-openai-key",
    anthropic_api_key="your-anthropic-key"
)
```

Environment variables are also supported:

```bash
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
```

## Structure

```bash
chat-analyzer/
├── README.md
├── pyproject.toml
├── chat_analyzer/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        
│   │   └── llm.py          
│   ├── analyzers/
│   │   ├── __init__.py 
│   │   ├── base.py         
│   │   ├── conversation.py  
│   │   ├── contact.py      
│   │   └── topic.py        
│   ├── models/
│   │   ├── __init__.py
│   │   └── schema.py       
│   └── utils/
│       ├── __init__.py
│       └── logger.py       
├── examples/
│   ├── analyze_chat.py
│   └── sample_data/
└── tests/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
