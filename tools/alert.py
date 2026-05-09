def send_alert(phone: str, data: dict, level: str):
    """真实环境中调用短信/电话接口，这里模拟打印"""
    print("\n" + "="*40)
    print(f"[紧急告警] 通知号码: {phone}")
    print(f"[紧急告警] 风险等级: {level}")
    print(f"[紧急告警] 数据: {data}")
    print("="*40 + "\n")
