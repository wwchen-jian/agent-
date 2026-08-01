from pydantic import BaseModel,Field,ValidationError
class student(BaseModel):
    name: str = Field(default = '不愿透露姓名' , description = '学生姓名' , min_length = 1 , max_length = 11 , examples = ["张三","李四"])
    age: int = Field(description = '学生的年龄要在8-18岁之间',le = 18,ge = 8,strict = True)
    phone: str = Field(description = '电话要求标准11位数字,中间可加空格和-', pattern = r"^1[3-9]\d{1}[ -]?\d{4}[ -]?\d{4}$")

try:
    xiaoming = student(name = '小明', age = 18 , phone = '138-4357-0055')
    print(xiaoming.phone)
except ValidationError as e:
    print(f"数据格式错误:{e}")
