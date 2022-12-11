from requests import Session


class API(Session):
    def __init__(self) -> None:
        super().__init__()
        self.response = None
        self.headers.update({"Content-Type": "application/json"})

    def print_log(self) -> None:
        print("\nREQUEST:")
        print(self.response.request.method, self.response.request.url)
        print(f"BODY:{self.response.request.body}")
        print("RESPONSE:")
        print(f"STATUS_CODE:{self.response.status_code}")
        print(f"TEXT:{self.response.text}\n")
