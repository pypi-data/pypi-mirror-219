from zs_utils.api.wildberries.base_api import WildberriesAPI


class GetWildberriesOrders(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace/paths/~1api~1v2~1orders/get
    """

    http_method = "GET"
    resource_method = "api/v2/orders"
    required_params = [
        "date_start",
        "take",
        "skip",
    ]
    allowed_params = [
        "date_end",
        "status",
        "id",
    ]


class GetWildberriesSupplies(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace/paths/~1api~1v2~1supplies/get
    """

    http_method = "GET"
    resource_method = "api/v2/supplies"
    required_params = [
        "status",
    ]


class GetWildberriesSupplyOrders(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace/paths/~1api~1v2~1supplies~1%7Bid%7D~1orders/get
    """

    http_method = "GET"
    resource_method = "api/v2/supplies/{supply_id}/orders"
    required_params = [
        "supply_id",
    ]


class GetWildberriesSupplyBarcode(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace/paths/~1api~1v2~1supplies~1%7Bid%7D~1barcode/get
    """

    http_method = "GET"
    resource_method = "api/v2/supplies/{supply_id}/barcode"
    required_params = [
        "supply_id",
        "type",
    ]


class GetWildberriesOrdersSVGStickers(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace/paths/~1api~1v2~1orders~1stickers/post
    """

    http_method = "POST"
    resource_method = "api/v2/orders/stickers"
    required_params = [
        "orderIds",
    ]


class GetWildberriesOrdersPDFStickers(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace/paths/~1api~1v2~1orders~1stickers~1pdf/post
    """

    http_method = "POST"
    resource_method = "api/v2/orders/stickers/pdf"
    required_params = [
        "orderIds",
    ]


class CreateWildberriesSupply(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace/paths/~1api~1v2~1supplies/post
    """

    http_method = "POST"
    resource_method = "api/v2/supplies"


class AddOrdersToWildberriesSupply(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace/paths/~1api~1v2~1supplies~1%7Bid%7D/put
    """

    http_method = "PUT"
    resource_method = "api/v2/supplies/{supply_id}"
    required_params = [
        "supply_id",
        "orders",
    ]


class CloseWildberriesSupply(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace/paths/~1api~1v2~1supplies~1%7Bid%7D~1close/post
    """

    http_method = "POST"
    resource_method = "api/v2/supplies/{supply_id}/close"
    required_params = [
        "supply_id",
    ]


class UpdateWildberriesOrdersStatus(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Marketplace/paths/~1api~1v2~1orders/put
    """

    http_method = "PUT"
    resource_method = "api/v2/orders"
    required_params = [
        "orderId",
        "status",
    ]
    allowed_params = [
        "sgtin",
    ]
