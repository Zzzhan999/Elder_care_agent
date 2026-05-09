from datetime import datetime
from memory.memory_store import MemoryStore
from llm.llm_client import LLMClient

class MedicationReminderAgent:
    def __init__(self, llm: LLMClient, memory: MemoryStore):
        self.llm = llm
        self.memory = memory

    def process(self, text: str):
        # 记录是否确认服药
        if "没吃" in text or "忘了" in text:
            self.memory.add_health_record({
                "type": "漏服",
                "timestamp": datetime.now().isoformat(),
                "note": text
            })
        elif "吃了" in text or "吃完" in text:
            self.memory.add_health_record({
                "type": "服药确认",
                "timestamp": datetime.now().isoformat()
            })
        # 实际环境中会主动设置日历提醒，这里略
