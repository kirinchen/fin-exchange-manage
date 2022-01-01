from dto import order_dto
from dto.order_dto import OrderDto
from infra import enums


def test_convert_to_model():
    dto = OrderDto()
    dto.side = enums.OrderSide.SELL
    ans = order_dto.convert_to_model(dto)
    print("ans=" + str(ans))
