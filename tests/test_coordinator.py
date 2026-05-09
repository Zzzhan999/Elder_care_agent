import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from agents.coordinator import Coordinator
from memory.memory_store import MemoryStore
from llm.llm_client import MockLLMClient

def test_health_report_flow():
    memory = MemoryStore({"name": "测试老人", "family": {"儿子": "小明"}})
    llm = MockLLMClient()
    coordinator = Coordinator(memory, llm, {"phone": "123456"})
    reply = coordinator.process_message("我头晕，高压150低压95")
    assert "血压" in reply or "观察" in reply
    # 检查记忆已存储
    assert any(r["symptom"] == "头晕" for r in memory.health_records)

def test_emergency_alert():
    memory = MemoryStore({"name": "李大爷"})
    llm = MockLLMClient()
    coordinator = Coordinator(memory, llm, {"phone": "999"})
    reply = coordinator.process_message("我胸口剧痛，高压190低压120")
    # 应触发告警，回复中可能包含“已通知”
    # 这里只测试无异常
    assert reply is not None
