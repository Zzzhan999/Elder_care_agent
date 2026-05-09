# Elder_care_agent
# AI 老人健康陪伴助手 (多Agent协作)

## 核心痛点
1. **健康监测无感化**：老年人抵触复杂App，需要将血压/血糖记录融入日常聊天。
2. **陪伴记忆缺失**：普通机器人不记得老人家庭、病史，对话冰冷。
3. **紧急响应矛盾**：关键词告警易误报，需要结合上下文与趋势的深度推理。

## 核心逻辑流
- **长链推理**：用户消息 → 意图识别 → 多源信息检索(记忆+RAG) → 风险评估(规则+LLM分层推演) → 多目标响应生成 → 状态更新。
- **多Agent协作**：`Coordinator`调度下面4个专业Agent，并行/串行执行后合并输出。
  - HealthRecordAgent：提取血压/血糖/症状
  - EmergencyAgent：基于数值+症状+历史进行风险分层
  - CompanionAgent：利用记忆生成带温度的回复
  - MedicationReminderAgent：管理用药提醒和依从记录

## 运行方式
1. 安装依赖：`pip install -r requirements.txt`
2. 配置大模型：编辑 `config.yaml` 填入API key，或使用模拟模式。
3. 启动：`python main.py`，输入文字模拟聊天。
4. 测试：`python -m pytest tests/`

## 技术栈
Python 3.10+ / LangChain(可选) / OpenAI API / 规则引擎
