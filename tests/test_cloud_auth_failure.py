"""Rejected cloud credentials must stop the login retries.

The Dreame account locks itself after 5 failed logins, so once the account
rejects the stored password the integration has to stop trying and ask the
user to re-authenticate.
"""

import base64
import json
import zlib
from types import SimpleNamespace

import pytest

from dreame import protocol as protocol_module
from dreame.device import DreameMowerDevice
from dreame.exceptions import DeviceAuthFailedException
from dreame.protocol import DreameMowerDreameHomeCloudProtocol

STRINGS = json.loads(
    zlib.decompress(base64.b64decode(protocol_module.DREAME_STRINGS), zlib.MAX_WBITS | 32)
)

PASSWORD_REJECTED = {
    "error": "limit_attempts_unauthorized",
    "error_description": "user password not match",
    "maxAttempts": "5",
    "remains": "4",
}
TOKEN_INVALID = {"error": "invalid_token", "error_description": "Token invalid"}
LOGIN_OK = {
    STRINGS[18]: "access-token",
    STRINGS[19]: "refresh-token-2",
    STRINGS[20]: 3600,
    "uid": "uid-1",
}


class FakeResponse:
    def __init__(self, status_code, body):
        self.status_code = status_code
        self.text = json.dumps(body)


class FakeSession:
    def __init__(self, responses, calls):
        self._responses = responses
        self._calls = calls

    def post(self, url, headers=None, data=None, timeout=None):
        self._calls.append(data)
        return self._responses.pop(0)

    def close(self):
        pass


@pytest.fixture
def cloud(monkeypatch):
    responses, calls = [], []
    monkeypatch.setattr(
        protocol_module.requests, "session", lambda: FakeSession(responses, calls)
    )
    proto = DreameMowerDreameHomeCloudProtocol("user@example.com", "secret", "eu")
    return proto, responses, calls


def test_rejected_password_stops_further_logins(cloud):
    proto, responses, calls = cloud
    responses.append(FakeResponse(400, PASSWORD_REJECTED))

    assert proto.login() is False
    assert proto.auth_failed is True

    # No new request may reach the account until the user re-authenticates.
    assert proto.login() is False
    assert proto.login() is False
    assert len(calls) == 1


def test_revoked_refresh_token_falls_back_to_password_once(cloud):
    proto, responses, calls = cloud
    proto._secondary_key = "refresh-token-1"
    responses.extend([FakeResponse(401, TOKEN_INVALID), FakeResponse(200, LOGIN_OK)])

    assert proto.login() is True
    assert proto.auth_failed is False
    assert len(calls) == 2
    assert "refresh-token-1" in calls[0]
    assert "refresh-token-1" not in calls[1]


def test_revoked_refresh_token_and_rejected_password(cloud):
    proto, responses, calls = cloud
    proto._secondary_key = "refresh-token-1"
    responses.extend(
        [FakeResponse(401, TOKEN_INVALID), FakeResponse(400, PASSWORD_REJECTED)]
    )

    assert proto.login() is False
    assert proto.auth_failed is True
    assert proto.login() is False
    assert len(calls) == 2


def test_server_error_is_not_a_credential_error(cloud):
    proto, responses, calls = cloud
    responses.append(FakeResponse(500, {"error": "server_error"}))

    assert proto.login() is False
    assert proto.auth_failed is False

    responses.append(FakeResponse(200, LOGIN_OK))
    assert proto.login() is True
    assert len(calls) == 2


class BareDevice(DreameMowerDevice):
    # The real interval is computed from the device status; a constant is enough here.
    _update_interval = 10


def make_device(auth_failed):
    device = object.__new__(BareDevice)
    device._update_running = False
    device._protocol = SimpleNamespace(cloud=SimpleNamespace(auth_failed=auth_failed))
    return device


def test_update_raises_without_logging_in_again():
    device = make_device(auth_failed=True)
    device.connect_cloud = lambda: pytest.fail("connect_cloud must not run")

    with pytest.raises(DeviceAuthFailedException):
        device.update()


def test_update_task_stops_polling_and_reports_the_error():
    device = make_device(auth_failed=True)
    device._update_timer = None
    device._update_fail_count = 0
    device._ready = True
    device.available = True
    device.disconnected = False
    errors, scheduled = [], []
    device._error_callback = errors.append
    device.schedule_update = lambda *args, **kwargs: scheduled.append(args)

    device._update_task()

    assert len(errors) == 1
    assert isinstance(errors[0], DeviceAuthFailedException)
    assert device.available is False
    assert scheduled == []
