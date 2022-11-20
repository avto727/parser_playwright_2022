# import configparser
# import json
# import os
# from configparser import ConfigParser
#
# import pytest
# import requests_to_curl
# from _pytest.config.argparsing import Parser
# from _pytest.fixtures import SubRequest
# from dotenv import load_dotenv
# from jsonpath_ng import parse as json_parse
# from pydantic import ValidationError
# from pytest_bdd import given, parsers, then, when
# from requests import Response
#
# from tests.core.api import API
# from tests.core.store import Store
# from tests.features.api.geomancer.geomancer_models import GeomancerModel
# from tests.features.api.maps.maps_models import MapsPlacesModel
# from utils.app_config import AppConfig
#
#
# load_dotenv()
#
#
# def pytest_addoption(parser: Parser) -> None:
#     parser.addoption(
#         "--cfg",
#         action="store",
#         default="",
#         help="you need select config from config directory",
#     )
#
#
# @pytest.fixture
# def client() -> None:
#     yield API()
#
#
# @pytest.fixture(scope="session")
# def config(request: SubRequest) -> ConfigParser:
#     config_name = request.config.getoption("--cfg")
#     if config_name != "":
#         config = configparser.ConfigParser()
#         config.read(config_name)
#     else:
#         config = AppConfig().get_config()
#     return config
#
#
# @given(
#     parsers.parse(
#         "send {method} to {host} to {endpoint} with {json_filename}"
#     ),
#     target_fixture="send_method_request",
# )
# def ak_send_method_request(
#         client: API,
#         config: ConfigParser,
#         method: str,
#         host: str,
#         endpoint: str,
#         json_filename: str,
# ) -> Response:
#     dir_client = {
#         "GET": client.get,
#         "get": client.get,
#         "POST": client.post,
#         "post": client.post,
#         "put": client.put,
#     }
#     env = config["MAIN"]["env"]
#     api_key = os.getenv(f"{env}_api_key")
#     url = f"{config['MAIN'][host]}{endpoint}{api_key}"
#     client.headers.update({"Content-Type": "application/json"})
#     with open(f"files/{json_filename}", encoding="utf-8-sig") as json_file:
#         data = json.load(json_file)
#         response = dir_client.get(method)(
#             url, json.dumps(data, indent=3), headers=client.headers
#         )
#     response_to_store("response", response, endpoint)
#     client.response = response
#     client.print_log()
#     request_to_curl(config, response)
#     return response
#
#
# @given(
#     parsers.parse(
#         "no api_key {method} to {host} to {endpoint} with {json_filename}"
#     ),
#     target_fixture="send_method_request",
# )
# def no_api_key_send_method_request(
#         client: API,
#         config: ConfigParser,
#         method: str,
#         host: str,
#         endpoint: str,
#         json_filename: str = "test.json",
# ) -> Response:
#     dir_client = {
#         "GET": client.get,
#         "get": client.get,
#         "POST": client.post,
#         "post": client.post,
#         "put": client.put,
#     }
#     client.headers.update({"Content-Type": "application/json"})
#     if method.upper() == "GET":
#         response = send_get_request(client, config, endpoint)
#     else:
#         with open(f"files/{json_filename}", encoding="utf-8-sig") as json_file:
#             data = json.load(json_file)
#             response = dir_client.get(method)(
#                 f"{config['MAIN'][host]}{endpoint}", json.dumps(data, indent=3)
#             )
#             client.response = response
#     response_to_store("response", response, endpoint)
#     client.response = response
#     client.print_log()
#     request_to_curl(config, response)
#     return response
#
#
# @when(
#     parsers.parse(
#         "Send {method} with header {json_filename} "
#         "to {host} with {endpoint} to store {key}"
#     )
# )
# def send_method_request_with_header(
#         client: API,
#         config: ConfigParser,
#         method: str,
#         json_filename: str,
#         host: str,
#         endpoint: str,
#         key: str,
# ) -> Response:
#     dir_client = {
#         "get": client.get,
#         "head": client.head,
#         "HEAD": client.head,
#         "post": client.post,
#         "put": client.put,
#     }
#     client.headers = {}
#     part = "/v3/suggest?limit=7&q=Mosco&"
#     env = config["MAIN"]["env"]
#     params = os.getenv(f"{env}_api_key")
#     client.headers.update({"X-Original-Uri": f"{part}{params}"})
#     url = f"{config['MAIN'][host]}{endpoint}{params}"
#     client.response = dir_client.get(method)(url)
#     response_to_store(key, client.response, endpoint)
#     client.print_log()
#     request_to_curl(config, client.response)
#     print(f"Step When Send {method} request {endpoint}")
#     return client.response
#
#
# @when(parsers.parse("Without store send {method} to {host} with {endpoint}"))
# def send_method_request_without_store(
#         client: API, config: ConfigParser, method: str, host: str,
#         endpoint: str
# ) -> Response:
#     dir_client = {
#         "GET": client.get,
#         "get": client.get,
#         "head": client.head,
#         "HEAD": client.head,
#         "post": client.post,
#         "put": client.put,
#     }
#     client.headers = {}
#     part = "/v3/suggest?limit=7&q=Mosco&"
#     env = config["MAIN"]["env"]
#     params = os.getenv(f"{env}_api_key")
#     client.headers.update({"X-Original-Uri": f"{part}{params}"})
#     url = f"{config['MAIN'][host]}{endpoint}"
#     client.response = dir_client.get(method)(url)
#     client.print_log()
#     print(f"Step When Send {method} request {endpoint} Without store ")
#     return client.response
#
#
# @when(parsers.parse("I send GET to {host} with {endpoint} to store {key}"))
# def send_get_request(
#         client: API,
#         config: ConfigParser,
#         host: str,
#         endpoint: str,
#         key: str = "nothing",
# ) -> Response:
#     if endpoint == "None":
#         endpoint = ""
#     url = f"{config['MAIN'][host]}{endpoint}"
#     print(url)
#     client.response = client.get(url)
#     client.print_log()
#     request_to_curl(config, client.response)
#     print(f"Step When I send GET request {endpoint}")
#     return client.response
#
#
# @when(
#     parsers.parse(
#         "Send GET with api_key to {host} with {endpoint} to store {key}"
#     )
# )
# def send_get_request_2(
#         client: API, config: ConfigParser, host: str, endpoint: str, key: str
# ):
#     store = Store()
#     env = config["MAIN"]["env"]
#     api_key = os.getenv(f"{env}_api_key")
#     url = f"{config['MAIN'][host]}{endpoint}{api_key}"
#     response = client.get(url)
#     client.response = response
#     client.print_log()
#     if (
#             "{" in response.text
#             and "png" not in endpoint
#             and "!doctype html" not in response.text.strip()
#     ):
#         res = response.json()
#         print(res)
#         store[key] = res
#     else:
#         res = response.text.strip()
#         print(f"This is not a json format\n{res}")
#     request_to_curl(config, response)
#     print(f"Step When I send GET request {endpoint}")
#     return response
#
#
# def response_to_store(key: str, response: Response, endpoint: str):
#     if "{" in response.text and "png" not in endpoint:
#         store = Store()
#         res = response.json()
#         print(res)
#         store[key] = res
#     else:
#         res = response.text.strip()
#         print(f"This is not a json format\n{res}")
#
#
# def request_to_curl(config: ConfigParser, response: Response) -> None:
#     env = config["MAIN"]["env"]
#     params = os.getenv(f"{env}_api_key")
#     api_key = params.split("api_key=")[1]
#     cp = requests_to_curl.parse(response)
#     if cp is not None:
#         curl = (
#             cp.replace(api_key, "YOUR_API_KEY")
#             .replace(
#                 "-H 'Accept: */*' -H 'Accept-Encoding: gzip, deflate' -H "
#                 "'Connection: keep-alive' ",
#                 "",
#             )
#             .replace(
#                 "-H 'Content-Type: application/json' -H 'User-Agent: "
#                 "python-requests/2.25.1'",
#                 "",
#             )
#             .replace("-H 'Content-Length: 396' ", "")
#         )
#         print(curl)
#     else:
#         print("requests_to_curl == None")
#
#
# @given(parsers.parse("assert status code is {code}"))
# @then(parsers.parse("assert status code is {code}"))
# def assert_status_code(client: API, code: str) -> None:
#     assert client.response.status_code == int(
#         code
#     ), f"\n{client.response.status_code} != \n{int(code)}"
#     print(f"Step Then assert status code is {code} PASS")
#
#
# @then(parsers.parse("assert body contains text {text}"))
# def assert_body_contains_text(client: API, text: str) -> None:
#     assert text.strip('"') in client.response.text.strip(
#         '"'
#     ), f"\n{text} NOT in \n{client.response.text}"
#     print(f'Step Then assert body contains text "{text}" PASS')
#
#
# @then(parsers.parse("assert prod_body contains text {text} dev_body {text_2}"))
# def assert_prod_dev_body_contains_text(
#         config: ConfigParser, client: API, text: str, text_2: str
# ) -> None:
#     host = config["MAIN"]["maps"]
#     if "dev" in host:
#         text = text_2
#     assert text.strip('"') in client.response.text.strip(
#         '"'
#     ), f"\n{text} NOT in \n{client.response.text}"
#     print(f'Step Then assert body contains text "{text}" PASS')
#
#
# @then(parsers.parse("assert body contains {key}"))
# def assert_body_contains_key(client: API, key: str) -> None:
#     assert (
#             key in client.response.json()
#     ), f"\n{key} in \n{client.response.json()}"
#     print(f"Step Then assert body contains key {key} PASS")
#
#
# @then(parsers.parse("assert body contains key list {key_list}"))
# def assert_body_contains_key_list(client: API, key_list: str) -> None:
#     key_list_m = [b for b in key_list.split(", ")]
#     for key in key_list_m:
#         assert (
#                 key in client.response.text
#         ), f"\n{key} NOT in \n{client.response.text}"
#     print(f'Step Then assert body contains text "{key_list}" PASS')
#
#
# @then(parsers.parse("assert in headers {key} equal {value}"))
# def assert_headers_key_equal(client: API, key: str, value: str) -> None:
#     assert value == client.response.headers.get(
#         key
#     ), f"\n{value} != \n{client.response.headers.get(key)}"
#     print(f"Step Then assert_headers key {key} equal {value} PASS")
#
#
# @then(parsers.parse("assert as str {key} equal str {value}"))
# def assert_equal_str(client: API, key: str, value: str) -> None:
#     response = client.response.json()
#     str_res = json.dumps(response)
#     el_key = f'"{key}": "{value}"'
#     counter = str_res.count(el_key)
#     assert counter == 1, f'"{key}": "{value}" not found'
#     print(f"Step Then assert {key} equal {value} PASS")
#
#
# @then(parsers.parse("assert as str {key} equal {value}"))
# def assert_equal_int(client: API, key: str, value: str) -> None:
#     response = client.response.json()
#     str_res = json.dumps(response)
#     el_int_value = f'"{key}": {value}'
#     counter = str_res.count(el_int_value)
#     assert counter == 1, f'"{key}": {value} not found'
#     print(f"Step Then assert {key} equal {value} PASS")
#
#
# @then(parsers.parse("assert body contains jsonpath {key} equal {value}"))
# def assert_response_contains_by_jsonpath(
#         client: API, key: str, value: str
# ) -> None:
#     json_expression = json_parse(f"results[*].{key}")
#     actual_value = json_expression.find(client.response.json())[0].value
#     assert (
#             actual_value == value
#     ), f"body not contains {key}={value}\n{key}={actual_value}"
#     print(f"Then assert body contains jsonpath {key} equal {value}")
#
#
# def assert_models(js_response: str, models_name: str) -> None:
#     dir_class = {
#         "geomancer": GeomancerModel,
#         "maps_places": MapsPlacesModel,
#     }
#     try:
#         dump_js = json.dumps(js_response)
#         valid = dir_class.get(models_name).parse_raw(dump_js)
#     except ValidationError as e:
#         print("Exception", e.json())
#     else:
#         print(valid.dict())
#
#
# @then(parsers.parse("assert Models {models_class}"))
# def receive_from_json_file(client: API, models_class: str) -> None:
#     js_response = client.response.json()
#     assert_models(js_response, models_class)
#     print(f"Then assert js_response {models_class} PASS")
