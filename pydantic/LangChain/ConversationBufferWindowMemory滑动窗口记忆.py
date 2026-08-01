import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_classic.chains import ConversationChain

memory = ConversationBufferWindowMemory(k = 2)
llm = ChatOpenAI(
    model = 'qwen-plus',
    api_key = os.getenv("DASHSCOPE_API_KEY"),
    base_url = 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    temperature = 0.1
)
conversation = ConversationChain(
    llm = llm,
    memory = memory,
    verbose = True
)

conversation.predict(input="数字：111")      # 1
conversation.predict(input="数字：222")      # 2
conversation.predict(input="数字：333")      # 3 窗口保留2、3，1被剔除
conversation.predict(input="数字：444")      # 4 窗口保留3、4，2被剔除
res = conversation.predict(input="我第一次发的数字是什么？") # AI回答333
print(res)
memory.clear()