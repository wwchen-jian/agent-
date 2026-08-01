import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_classic.chains import ConversationChain
from langchain_classic.memory import ConversationSummaryMemory

llm = ChatOpenAI(
    model='qwen-plus',
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
    temperature=0.1
)

memory = ConversationSummaryMemory(llm=llm)
conversation = ConversationChain(
    llm = llm,
    memory = memory,
    verbose = True,
)
for i in range(10):
    conversation.predict(input=f"告诉我关于Python的第{i+1}个知识点")

# 查看摘要内容
print("\n【当前记忆摘要】")
print(memory.buffer)