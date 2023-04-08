import base64


def get_base64_string(string: str) -> str:
    return base64.b64decode(string.encode("utf-8")).decode("utf-8")
