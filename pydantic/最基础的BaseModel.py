from pydantic import BaseModel
class person(BaseModel):
    name:str
    age:int
    phone:str
zhangsan = person(name = 'zhangsan', age = 20,phone = '12345678910')
print(zhangsan.name)
print(zhangsan.age)
print(zhangsan.phone)

#代码报错,phone不为str类型,age会强制转换为int类型
xiaoming = person(name = 'xiaoming', age = "18",phone = 10987654321)
print(xiaoming.age)
print(type(xiaoming.age))
