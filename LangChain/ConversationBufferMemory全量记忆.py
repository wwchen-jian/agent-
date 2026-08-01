import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_classic.chains import ConversationChain
from langchain_classic.memory import ConversationBufferMemory
llm = ChatOpenAI(
    model = 'qwen-plus',
    api_key = os.getenv("DASHSCOPE_API_KEY"),
    base_url = 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    temperature = 0.1
)

memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm = llm,
    memory = memory,
    #verbose = True
)

res1 = conversation.predict(input = '我叫小明,我今年20岁,你叫什么名字?')
print(res1)

res2 = conversation.predict(input = '我叫什么名字,今年多少岁?')
print(res2)

res3 = conversation.predict(input = '我刚刚说了什么个人信息?')
print(res3)

print(f"原始对话记录:{memory.chat_memory.messages}")

#清空记忆
memory.clear()