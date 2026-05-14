from __future__ import annotations

import hashlib
import os

P_FIELD = 2**127 - 1
B_CURVE = (-17) % P_FIELD
WINDOW = 2**16
ITEM_LIMIT = P_FIELD // WINDOW
ACCOUNT_NAME = b"admin"
ACCOUNT_ID = int.from_bytes(hashlib.sha256(ACCOUNT_NAME).digest(), "big") % ITEM_LIMIT
FLAG = os.environ.get("FLAG", "flag{test}")
