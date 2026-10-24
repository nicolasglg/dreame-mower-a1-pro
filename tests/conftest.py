import sys
from unittest.mock import MagicMock

# Provide stubs for dependencies that are not installed in the lightweight test environment
for mod in [
    "miio",
    "miio.miioprotocol",
    "Crypto",
    "Crypto.Cipher",
    "Crypto.Util",
    "Crypto.Util.Padding",
    "paho",
    "paho.mqtt",
    "paho.mqtt.client",
    "py_mini_racer",
    "pybase64",
]:
    if mod not in sys.modules:
        sys.modules[mod] = MagicMock()
