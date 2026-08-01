from langchain_core.prompts import PromptTemplate

template = PromptTemplate(
    input_variables=['commoidty','price'],
    template = '请为{commodity}提供一段吸引人的促销词,突出其{price}价格的性价比'
)

prompt = template.format(commodity = '西瓜' , price = '20')
print(prompt)