"""主入口：命令行对话模拟，可替换为微信/Web钩子"""
import os
import sys
sys.path.append(os.path.dirname(__file__))

from agents.coordinator import Coordinator
from memory.memory_store import MemoryStore
from llm.llm_client import get_llm_client
import yaml

def load_config():
    with open('config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def main():
    config = load_config()
    memory = MemoryStore(config['user'])
    llm = get_llm_client(config['llm'])
    coordinator = Coordinator(memory, llm, config.get('alert'))

    print("=== 老人健康陪伴助手 ===")
    print("输入文字聊天（q 退出）")
    while True:
        try:
            user_input = input("老人: ")
            if user_input.strip().lower() == 'q':
                break
            reply = coordinator.process_message(user_input)
            print(f"助手: {reply}\n")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"系统错误: {e}")

if __name__ == "__main__":
    main()
