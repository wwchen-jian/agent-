import json
import os
from dotenv import load_dotenv
from pydantic import PrivateAttr

load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import ConversationChain
from langchain_core.messages import HumanMessage, AIMessage

HISTORY_FILE = 'chat_history.json'

class PersistJsonMemory(ConversationBufferMemory):
    """
        支持 JSON 持久化的自定义记忆类
        - 初始化时自动加载历史
        - 每轮对话后自动保存
        - 带异常防护，文件损坏不崩溃
    """
    # 私有属性必须 _ 开头
    _file_path: str = PrivateAttr()
    _auto_save_every: int = PrivateAttr()
    _save_count: int = PrivateAttr()

    def __init__(self, file_path, auto_save_every = 1):
        super().__init__()
        self._file_path = file_path
        self._auto_save_every = auto_save_every
        self._save_count = 0
        self.load_history_from_json()

    def load_history_from_json(self):
        if not os.path.exists(self._file_path):
            print("未找到历史对话记录,自动开启新对话")
            return
        try:
            with open(self._file_path,'r',encoding='utf-8') as f:
                data = json.load(f)
            for i in data:
                if i.get('type') == 'human':
                    self.chat_memory.add_message(HumanMessage(content = i['content']))
                elif i.get('type') == 'ai':
                    self.chat_memory.add_message(AIMessage(content = i['content']))
            print(f"已成功加载{len(data)}条历史对话")
        except Exception as e:
            print(f"历史记录读取失败,已重置:{e}")
            if os.path.exists(self._file_path):
                os.rename(self._file_path,self._file_path + '.bak')

    def save_history_to_json(self):
        messages_list = []
        for i in self.chat_memory.messages:
            if isinstance(i,HumanMessage):
                messages_list.append({'type' : 'human', 'content' : i.content})
            elif isinstance(i,AIMessage):
                messages_list.append({'type' : 'ai', 'content' : i.content})
        with open(self._file_path,'w',encoding='utf-8') as f:
            json.dump(messages_list,f,ensure_ascii=False,indent=2)

    def save_context(self, inputs, outputs):
        super().save_context(inputs,outputs)
        self._save_count += 1
        if self._save_count % self._auto_save_every == 0:
            self.save_history_to_json()

llm = ChatOpenAI(
    model = 'qwen-plus',
    api_key = os.getenv("DASHSCOPE_API_KEY"),
    base_url = 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    temperature = 0.7
)
persist_memory = PersistJsonMemory(file_path=HISTORY_FILE)
chat_bot = ConversationChain(
    llm = llm,
    memory = persist_memory
)

def run_chatbot():
    print("持久化聊天机器人工作ing...")
    print("输入exit/bye/退出 即可保存退出\n")
    while True:
        user_input = input("用户:").strip()
        if user_input.lower() in ['exit','bye','退出']:
            persist_memory.save_history_to_json()
            print("下次见!(历史记录已保存)")
            break
        if not user_input:
            continue
        res = chat_bot.predict(input=user_input)
        print(f"AI:{res}")

if __name__ == "__main__":
    run_chatbot()