import json
from typing import Any


class Store:
    def __init__(self) -> None:
        with open("files/store.json", "w", encoding="utf-8-sig") as file:
            json.dump({}, file)

    def __setitem__(self, key: str, value: Any) -> None:
        with open("files/store.json", encoding="utf-8-sig") as json_file:
            data = json.load(json_file)
        data.update({key: value})
        with open("files/store.json", "w", encoding="utf-8-sig") as file:
            json.dump(
                data, file, indent=2, ensure_ascii=False, separators=(",", ":")
            )

    def __getitem__(self, item: str) -> str:
        with open("files/store.json", encoding="utf-8-sig") as json_file:
            data = json.load(json_file)
        return data.get(item)
