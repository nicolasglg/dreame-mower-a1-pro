import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

from dreame.device import DreameMowerDeviceStatus
from dreame.types import A1_PRO_STATUS_CODES, DreameMowerErrorCode, DreameMowerProperty

CONFIG_FLOW_SOURCE = (
    Path(__file__).parents[1] / "custom_components" / "dreame_mower" / "config_flow.py"
)


def make_status(error_value):
    status = object.__new__(DreameMowerDeviceStatus)
    status._get_property = lambda prop: (
        error_value if prop is DreameMowerProperty.ERROR else None
    )
    return status


@pytest.mark.parametrize("code", [53, 54, 70, 72])
def test_a1_pro_status_codes_are_not_errors(code):
    status = make_status(code)

    assert code in A1_PRO_STATUS_CODES
    assert status.error is DreameMowerErrorCode.NO_ERROR


def test_trapped_is_still_reported_as_error():
    status = make_status(DreameMowerErrorCode.TRAPPED.value)

    assert status.error is DreameMowerErrorCode.TRAPPED


def test_options_flow_does_not_assign_config_entry():
    tree = ast.parse(CONFIG_FLOW_SOURCE.read_text())
    handler = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
        and node.name == "DreameMowerOptionsFlowHandler"
    )

    for node in ast.walk(handler):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                assert not (
                    isinstance(target, ast.Attribute) and target.attr == "config_entry"
                ), "OptionsFlow.config_entry is read-only on recent Home Assistant"

    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "DreameMowerOptionsFlowHandler"
    ]
    assert calls and all(not call.args for call in calls)
