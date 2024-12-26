from typing import Dict, Any, List, Union, Optional
import logging
import json
import backoff
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

logger = logging.getLogger(__name__)

class LLMClient:
    """统一的 LLM 客户端
    支持 OpenAI 和 Anthropic 的模型
    """
    
    def __init__(self, openai_api_key: str = None, anthropic_api_key: str = None):
        self.openai_client = AsyncOpenAI(api_key=openai_api_key) if openai_api_key else None
        self.anthropic_client = AsyncAnthropic(api_key=anthropic_api_key) if anthropic_api_key else None
        
        # 记录已配置的模型
        logger.info("LLM clients initialized:")
        logger.info(f"OpenAI API: {'configured' if openai_api_key else 'missing'}")
        logger.info(f"Anthropic API: {'configured' if anthropic_api_key else 'missing'}")
        
        # 模型配置
        self.MODEL_CONFIGS = {
            "gpt-4": {
                "provider": "openai",
                "params": {"response_format": {"type": "json_object"}}
            },
            "claude-3-sonnet": {
                "provider": "anthropic",
                "params": {"max_tokens": 1024}
            }
        }

    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=3
    )
    async def analyze(
        self,
        prompt: str,
        model: str = "gpt-4",
        temperature: float = 0.3,
        **kwargs
    ) -> Dict[str, Any]:
        """统一的分析接口"""
        if model not in self.MODEL_CONFIGS:
            raise ValueError(f"Unsupported model: {model}")
            
        config = self.MODEL_CONFIGS[model]
        provider = config["provider"]
        
        # 合并参数
        params = {
            "temperature": temperature,
            **config["params"],
            **kwargs
        }
        
        try:
            if provider == "openai":
                return await self._call_openai(model, prompt, **params)
            else:
                return await self._call_anthropic(model, prompt, **params)
        except Exception as e:
            logger.error(f"Analysis failed with {model}: {str(e)}")
            raise

    async def _call_openai(self, model: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """调用 OpenAI API"""
        messages = [{"role": "user", "content": prompt}]
        response = await self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        return json.loads(response.choices[0].message.content)

    async def _call_anthropic(self, model: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """调用 Anthropic API"""
        response = await self.anthropic_client.messages.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return json.loads(response.content[0].text)
