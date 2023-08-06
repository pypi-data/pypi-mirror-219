from uuid import uuid4

from zs_utils.api.base_api import BaseAPI


class WildberriesAPI(BaseAPI):
    production_api_url = "https://suppliers-api.wildberries.ru/"

    def __init__(self, api_token: str, **kwargs):
        super().__init__(**kwargs)

        self.api_token = api_token

    @property
    def headers(self) -> dict:
        return {"Content-Type": "application/json", "Authorization": self.api_token}

    def get_request_params(self, **kwargs) -> dict:
        request_params = {
            "url": self.build_url(kwargs),
            "headers": self.headers,
        }

        clean_params = self.get_clean_params(kwargs)

        if self.http_method == "GET":
            request_params["params"] = clean_params
        else:
            if self.array_payload:
                request_params["json"] = clean_params["array_payload"]
            else:
                clean_params.update(
                    {
                        "id": str(uuid4()),
                        "jsonrpc": "2.0",
                    }
                )
                request_params["json"] = clean_params

        return request_params
