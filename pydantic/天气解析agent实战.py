import json
from pydantic import BaseModel,ValidationError,Field
import os
import requests
from dotenv import load_dotenv
load_dotenv()

class Weather(BaseModel):
    city : str = Field(description = "城市名称" , examples = ['北京' , '深圳' , '沈阳'])
    weather : str = Field(description = "当前城市的天气状况" , examples = ['晴','多云','雨'])
    temperature : int = Field(description = "当前城市的温度",ge = -50 , le = 50)
    wind : str = Field(default = "无风" , description = "描述当前风的等级",examples = ["微风","三级","无风"])

class llmclient :
    def __init__(self):
        self.key = os.getenv("DASHSCOPE_API_KEY")
        self.url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
        self.headers = {"Authorization": f"Bearer {self.key}" , "Content-Type": "application/json"}

    def chat(self , prompt , temp = 0.3):
        payload = {
            'model':'qwen-plus',
            "messages" : [
                {'role' : 'system' , 'content' : '你是一个智能天气信息提取助手'},
                {"role" : 'user' , 'content' : prompt},
            ],
            'temperature': temp
        }
        res = requests.post(self.url , json = payload , headers = self.headers)
        return res.json()['choices'][0]['message']['content']

def parse_weather(user_input):
    """
    让LLM从用户输入中提取天气信息,强制按照上面的格式以JSON形式返回,无多余文字
    :param user_input:用户输入的信息
    :return:LLM输出结果
    """
    prompt = f"""
    你是一个天气信息提取助手,仅根据用户输入的天气中提取真实信息,严禁自我编造数据,以JSON格式返回,不要做其他任何解释描述,只输出纯净JSON,格式如下:
    {{
        "city" : 城市
        "weather" : 天气情况
        "temperature" : 温度
        "wind" : 风力情况(默认无风)
    }}
    字段要求:
    city:输出所描述天气的城市,如北京,深圳,沈阳
    weather:输出天气情况,如晴,多云,雨
    temperature:输出温度,范围在-50与50摄氏度之间
    wind:风力,如三级,微风,无风
    严格输出纯净JSON,原文中没有提到的信息,直接删掉对应的JSON键
    用户输入:{user_input}
    """
    llm = llmclient()
    result = llm.chat(prompt = prompt)
    print(f"llm原始输出:\n{result}\n")
    res = result.strip()
    try:
        answer = Weather.model_validate_json(res)
        return answer
    except ValidationError as e:
        print(f"格式错误:{e}")
        return None

if __name__ == "__main__":
    try:
        userinput = "今天沈阳天气太糟糕了,一直在下雨,气温低到了6摄氏度,还刮了三级风,都不能出去玩了!"
        result = parse_weather(userinput)
        print(f"解析成功!解析结果:{result.model_dump_json()}")
        print(f"城市:{result.city}")
        print(f"天气:{result.weather}")
        print(f"温度:{result.temperature}摄氏度")
        print(f"风力:{result.wind}")
        #异常输入
        bad_input = '北京天气好晒啊,温度好高'
        result = parse_weather(bad_input)
        print(result)
    except Exception as e:
        print(f"捕获到异常{e}")