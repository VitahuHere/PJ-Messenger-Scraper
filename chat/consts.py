import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

TIMEOUT = 15
COOKIES = str(os.path.join(ROOT_DIR, ".wdm", "cookies.pkl"))
CRED_CACHE_DIR = str(os.path.join(ROOT_DIR, ".wdm"))


class FacebookConsts:
    DECLINE_COOKIES = 'data-cookiebanner="accept_only_essential_button"'
    SENT_SVG = (
        'd="m15.982 8.762-5.482 5.487-2.482-2.478a.75.75 0 0 0 -1.06 1.06l3.008 '
        '3.008a.748.748 0 0 0 1.06 0l6.016-6.016a.75.75 0 0 0 -1.06-1.061z"'
    )
    DELIVERED_SVG = (
        'd="m12 2a10 10 0 1 0 10 10 10.011 10.011 0 0 0 -10-10zm5.219 8-6.019 6.016a1 1 0 0 1 '
        '-1.414 0l-3.005-3.008a1 1 0 1 1 1.419-1.414l2.3 2.3 5.309-5.31a1 1 0 1 1 1.41 1.416z"'
    )
    TEXT_BOX = 'role="textbox"'
    IMAGE_BOX = 'type="file"'
    EMAIL_ID = "email"
    PASS_ID = "pass"
    MESSAGE_ROW = "role=row"


class PJConsts:
    ...
