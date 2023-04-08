__author__ = "Cong Minh Vu"
__version__ = "1.0.0"
__license__ = "GNU General Public License v3.0"


import base64


def get_base64_string(string: str) -> str:
    return base64.b64decode(string.encode("utf-8")).decode("utf-8")
