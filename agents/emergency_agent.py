from typing import Tuple, Dict
from memory.memory_store import MemoryStore

class EmergencyAgent:
    def assess(self, record: dict, memory: MemoryStore) -> dict:
        """返回 {'level': str, 'should_alert': bool}"""
        systolic = record.get("systolic", 0)
        diastolic = record.get("diastolic", 0)
        symptom = record.get("symptom", "")

        # 规则1：极高值直接告警
        if systolic >= 180 or diastolic >= 110:
            return {"level": "高危（血压极高）", "should_alert": True}

        # 规则2：高值伴严重症状告警
        if systolic >= 160 and ("胸痛" in symptom or "呼吸困难" in symptom or "摔倒" in symptom):
            return {"level": "高危（高压+危险症状）", "should_alert": True}

        # 规则3：结合近期趋势的中等风险推理
        if systolic >= 145:
            recent_records = memory.get_recent_health(days=3, fields=["systolic"])
            high_count = sum(1 for r in recent_records if r.get("systolic", 0) >= 145)
            if high_count >= 2:
                return {"level": "中高风险（持续偏高）", "should_alert": False}
            return {"level": "中低风险", "should_alert": False}

        # 规则4：低血压合并晕厥前兆
        if systolic <= 90 and ("头晕" in symptom or "发黑" in symptom):
            return {"level": "低血压风险", "should_alert": False}

        return {"level": "低风险", "should_alert": False}
