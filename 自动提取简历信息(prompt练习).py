#五大类prompt:
#1. 角色设定 Prompt
#2. Few-Shot 少样本提示
#3. CoT 思维链
#4. 格式约束 Prompt
#5. 指令分级

#套用day1基础调用类

import os
import requests
from dotenv import load_dotenv
load_dotenv()
import json
class LLMClient():
    def __init__(self):
        self.key = os.getenv('DASHSCOPE_API_KEY')
        self.url = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'
        self.headers = {"Authorization": f"Bearer {self.key}",'Content-Type': 'application/json'}

    def chat(self,prompt,temp = 0.1):
        messages = [{"role": "user", "content": prompt}]
        payload = {
            'model' : 'qwen-plus',
            'messages' : messages,
            'temperature' : temp,
        }
        res = requests.post(self.url,headers = self.headers,json = payload)
        ans = res.json()["choices"][0]['message']["content"]
        return ans

if __name__ == "__main__":
    llm = LLMClient()
    input_txt = '王一,计算机科学与技术专业,211,熟练使用python,RAG,langchain,希望投递大模型开发实习'
    res = llm.chat(f"""你是一个简历信息提取工具严格遵守规则:
    1.角色设定:只输出纯净的json格式,不要做其他任何解释,描述,标题,严格
    2.指令分级:
        第一步cot推理,逐行提取姓名,学历与专业,技术栈,求职意向
        第二步整理字段,
        第三步仅输出JSON,禁止多余文字
    3.cot思维链:先定位姓名,再提取学历与专业,再拆分用户所有的技术技能为一个数组,再锁定求职的岗位(缺失内容填充空字符串)
    4.few-shot示例:
        输入:李二，本科软件工程，会Java、MySQL，求职后端开发
        输出：{{"name":"李二","education":"本科软件工程","skill":["Java","MySQL"],"intention":"后端开发"}}
    5.格式强制约束:必须输出纯净json
        输出固定字段:
            姓名:输出用户的姓名
            学历与专业:输出用户的学历与专业
            技术栈:输出用户所会的技能(用数组格式)
            求职意向:输出用户所想要求得职位
            (以上信息无对应信息填充空字符串)
    用户的自我介绍:{input_txt}
""")
    print(res)
    data = json.loads(res)
    print("存入json文件结果:")
    print(data)
    with open("resume_result.txt","w",encoding = 'utf-8') as f:
        json.dump(data,f,ensure_ascii = False,indent = 2)
    print("\n文件写入完成")