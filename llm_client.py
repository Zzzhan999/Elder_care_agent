"""LLM 客户端，支持真实API和模拟模式"""
from typing import Optional
import openai
import json

class LLMClient:
    def chat(self, messages: list, temperature=0.7) -> str:
        raise NotImplementedError

class OpenAIClient(LLMClient):
    def __init__(self, model: str, api_key: str, base_url: Optional[str] = None):
        self.model = model
        openai.api_key = api_key
        if base_url:
            openai.api_base = base_url

    def chat(self, messages: list, temperature=0.7) -> str:
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content

class MockLLMClient(LLMClient):
    """模拟LLM，用于演示"""
    def chat(self, messages: list, temperature=0.7) -> str:
        # 根据最后一条用户消息返回模拟结果
        last_msg = messages[-1]['content'].lower()
        if '提取健康数据' in last_msg:
            return '{"systolic": 145, "diastolic": 90, "symptom": "头晕"}'
        elif '风险评估' in last_msg:
            return '中等风险，需观察'
        elif '生成回复' in last_msg:
            return "阿姨，血压比昨天高了一点，是不是没休息好？今天先观察，记得限盐。"
        else:
            return "好的，我记下了。"

def get_llm_client(cfg: dict) -> LLMClient:
    if cfg.get('provider') == 'mock':
        return MockLLMClient()
    return OpenAIClient(
        model=cfg['model'],
        api_key=cfg['api_key'],
        base_url=cfg.get('base_url')
    )
