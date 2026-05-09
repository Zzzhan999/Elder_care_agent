"""记忆库：用户画像、健康记录、对话历史"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class MemoryStore:
    def __init__(self, user_profile: dict):
        self.profile = user_profile
        self.health_records: List[dict] = []
        self.conversation_history: List[dict] = []

    def add_health_record(self, record: dict):
        self.health_records.append({**record, "recorded_at": datetime.now().isoformat()})

    def get_recent_health(self, days: int = 7, fields: Optional[List[str]] = None) -> List[dict]:
        cutoff = datetime.now() - timedelta(days=days)
        recent = []
        for r in self.health_records:
            t = datetime.fromisoformat(r["recorded_at"])
            if t > cutoff:
                item = {k: v for k, v in r.items() if not fields or k in fields}
                recent.append(item)
        return recent

    def recall_by_keyword(self, keyword: str) -> Optional[str]:
        for r in reversed(self.health_records):
            if keyword in r.get("symptom", ""):
                return f"上次提到'{keyword}'是在{r['recorded_at']}，当时血压{r.get('systolic', '?')}/{r.get('diastolic', '?')}。"
        return None

    def add_conversation(self, role: str, text: str):
        self.conversation_history.append({"role": role, "content": text, "time": datetime.now().isoformat()})

    def recent_conversations(self, n=5):
        return self.conversation_history[-n:]
