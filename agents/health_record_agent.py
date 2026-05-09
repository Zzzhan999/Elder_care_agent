import json
from memory.memory_store import MemoryStore
from llm.llm_client import LLMClient

class HealthRecordAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def extract_and_store(self, text: str, memory: MemoryStore) -> dict:
        # 调用LLM抽取结构化数据
        prompt = (
            "从以下老人说的话中提取血压值和症状，以JSON返回。"
            "如果缺失则填0。格式：{\"systolic\": 收缩压, \"diastolic\": 舒张压, \"symptom\": \"症状\"}\n"
            f"用户输入：{text}"
        )
        messages = [{"role": "user", "content": prompt}]
        llm_output = self.llm.chat(messages, temperature=0)
        try:
            data = json.loads(llm_output)
        except json.JSONDecodeError:
            # 备用规则
            import re
            bp = re.findall(r'高压\s*(\d+).*?低压\s*(\d+)', text)
            systolic = int(bp[0][0]) if bp else 0
            diastolic = int(bp[0][1]) if bp else 0
            symptom = "头晕" if "头晕" in text else ""
            data = {"systolic": systolic, "diastolic": diastolic, "symptom": symptom}
        # 存储
        memory.add_health_record({
            "type": "血压",
            "systolic": data.get("systolic", 0),
            "diastolic": data.get("diastolic", 0),
            "symptom": data.get("symptom", "")
        })
        return data
