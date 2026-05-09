"""总调度器，实现长链推理与多Agent协作"""
import json
from typing import Dict
from .health_record_agent import HealthRecordAgent
from .emergency_agent import EmergencyAgent
from .companion_agent import CompanionAgent
from .medication_reminder_agent import MedicationReminderAgent
from memory.memory_store import MemoryStore
from llm.llm_client import LLMClient
from tools.alert import send_alert

class Coordinator:
    def __init__(self, memory: MemoryStore, llm: LLMClient, alert_config: dict = None):
        self.memory = memory
        self.llm = llm
        self.alert_config = alert_config or {}
        self.health_agent = HealthRecordAgent(llm)
        self.emergency_agent = EmergencyAgent()
        self.companion_agent = CompanionAgent(llm)
        self.med_agent = MedicationReminderAgent(llm, memory)

    def process_message(self, user_text: str) -> str:
        # --- 长链推理第一步：意图识别 ---
        intent = self._detect_intent(user_text)

        # --- 长链推理第二步：多Agent分发与并行处理 ---
        health_data = {}
        risk_info = {"level": "无", "should_alert": False}

        if intent == "health_report":
            # Agent1: 健康数据抽取
            health_data = self.health_agent.extract_and_store(user_text, self.memory)
            # Agent2: 紧急风险评估（结合历史）
            risk_info = self.emergency_agent.assess(health_data, self.memory)
            if risk_info["should_alert"]:
                self._trigger_alert(health_data, risk_info["level"])

        elif intent == "medication":
            # Agent3: 用药确认或提醒设置
            self.med_agent.process(user_text)
            risk_info["level"] = "用药记录"

        # --- 长链推理第三步：陪伴对话生成（无论哪种意图都执行） ---
        # Agent4: 利用记忆+健康数据+风险生成回复
        response = self.companion_agent.generate(
            user_text=user_text,
            health_data=health_data,
            risk=risk_info["level"],
            memory=self.memory
        )

        # --- 第四步：更新记忆 ---
        self.memory.add_conversation("user", user_text)
        self.memory.add_conversation("assistant", response)

        return response

    def _detect_intent(self, text: str) -> str:
        # 简化意图分类，实际可调用 LLM 或规则
        health_keywords = ["血压", "高压", "低压", "血糖", "头晕", "胸闷", "摔倒", "体温"]
        med_keywords = ["药", "吃药", "忘", "没吃", "提醒"]
        if any(w in text for w in health_keywords):
            return "health_report"
        if any(w in text for w in med_keywords):
            return "medication"
        return "chat"

    def _trigger_alert(self, data: dict, level: str):
        """紧急告警，通知家属"""
        phone = self.alert_config.get("phone", "")
        send_alert(phone, data, level)
        # 记录告警事件
        self.memory.add_health_record({"type": "alert", "level": level, "data": data})
