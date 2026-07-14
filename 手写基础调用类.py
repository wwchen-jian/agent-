import os
import requests
from dotenv import load_dotenv
load_dotenv()

class LLMClient:
    def __init__(self):
        self.key = os.getenv("DASHSCOPE_API_KEY")
        self.url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
        self.headers = {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"}
        #支持多轮对话
        self.history = [{"role" : "system", "content" : "you are a helpful assistant"}]
    def chat(self,prompt,temp=0.7):
        self.history.append({"role":"user","content":prompt})
        payload = {
            'model' : 'qwen-plus',
            'messages' : self.history,
            "temperature": temp,
        }
        res = requests.post(self.url,headers = self.headers,json = payload)
        answer = res.json()["choices"][0]["message"]["content"]
        self.history.append({"role":"assistant","content":answer})
        return answer

    def reset_history(self):#重置对话
        self.history.clear()
        history = [{"role":"system","content":"you are a helpful assistant"}]
if __name__ == "__main__":
    llm = LLMClient()
    print(llm.chat("我叫小明"))
    print(llm.chat("我叫什么名字"))
    llm.reset_history()
    print(llm.chat("我叫什么名字"))