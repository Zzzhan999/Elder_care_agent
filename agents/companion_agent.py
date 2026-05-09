from memory.memory_store import MemoryStore
from llm.llm_client import LLMClient

class CompanionAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def generate(self, user_text: str, health_data: dict, risk: str, memory: MemoryStore) -> str:
        # 记忆检索：上次相关症状、家庭信息
        recall = ""
        if health_data.get("symptom"):
            recall = memory.recall_by_keyword(health_data["symptom"]) or ""
        family_info = str(memory.profile.get("family", {}))
        recent_dialogs = memory.recent_conversations(3)

        system_prompt = (
            "你是贴心的老年健康陪伴助手，语气温暖、自然，像家人一样。"
            f"你了解用户：{memory.profile}。"
            "根据上下文、健康数据和风险等级，生成恰当的回复，可以包含关切、轻度健康建议和情感支持。"
            "不要使用医学术语轰炸，要口语化。如果风险较高，适当安抚并告知已联系家人。"
        )
        user_prompt = (
            f"用户刚刚说：“{user_text}”\n"
            f"抽取的健康数据：{health_data}\n"
            f"当前风险评估：{risk}\n"
            f"相关记忆：{recall}\n"
            f"最近对话：{recent_dialogs}\n"
            "请生成回复："
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        return self.llm.chat(messages, temperature=0.7)
