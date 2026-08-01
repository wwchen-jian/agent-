import json
from pydantic import BaseModel , ValidationError

class person(BaseModel):
    name:str
    age:int
    email:str

llm_output = '{"name" : "zhangsan" , "age" : 11 , "email" : "123456@qq.com"}'
try:
    #方法1 : 先loads再解包
    data = json.loads(llm_output)
    p1 = person(**data)

    #方法2 : 用model_validate
    p2 = person.model_validate(data)

    #方法3 : 从JSON字符串直接解析
    p3 = person.model_validate_json(llm_output)

    print(p1)
    print(p2)
    print(p3)
    print(p1.model_dump())
    print(p2.model_dump())
    print(p3.model_dump())
    print(p1.model_dump_json())
    print(p2.model_dump_json())
    print(p3.model_dump_json())

except ValidationError as e:
    print(e)
