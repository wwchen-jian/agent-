from pydantic import BaseModel,computed_field,ValidationError
from typing import List

class commodity(BaseModel):
    name: str
    price: float
class shopping_cart(BaseModel):
    name:str
    commodities:list[commodity]

    @computed_field(return_type = float)
    @property
    def total_price(self) -> float:
        total = 0.0
        for i in self.commodities:
            total+=i.price
        return total

try:
    zhangsan = shopping_cart(
        name = '张三',
        commodities = [
            commodity(name = "汉堡", price = 10.00),
            commodity(name = '薯条' , price = 5.00),
            commodity(name = '无糖可乐' , price = 2.50),
        ]
    )
    print(zhangsan.name)
    print(zhangsan.commodities)
    print(zhangsan.total_price)
    print(zhangsan.model_dump_json(indent = 2))
except ValidationError as e:
    print(f"数据格式错误:{e}")