import sys
from unittest.mock import MagicMock

# Stub external dependencies only when they are not installed in the test environment.
# Kept strictly minimal so real import errors in existing tests are not masked.
for mod in [
    "miio",
    "miio.miioprotocol",
    "py_mini_racer",
]:
    if mod not in sys.modules:
        try:
            __import__(mod)
        except ImportError:
            sys.modules[mod] = MagicMock()
