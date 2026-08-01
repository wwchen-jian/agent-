from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
load_dotenv()

llm = ChatOpenAI(
    model = 'qwen-plus',
    api_key = os.getenv("DASHSCOPE_API_KEY"),
    base_url = 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    temperature = 0.7
)
#print(llm)
prompt = PromptTemplate(
    input_variables = ["text"],
    template = '请用英语翻译以下内容:\n{text}'
)

#print(prompt)
chain = prompt | llm
#print(chain)

result = chain.invoke({'text' : '人工智能浪潮'})
print(result.content)
