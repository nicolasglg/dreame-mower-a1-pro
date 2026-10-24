from types import SimpleNamespace
from unittest.mock import Mock, call
import pytest

from dreame.device import DreameMowerDevice
from dreame.const import (
    MOWING_PREFERENCE_CUTTING_HEIGHT_INDEX,
    MOWING_PREFERENCE_GLOBAL_AREA_ID,
    MOWING_PREFERENCE_MAP_INDEX_INDEX,
    MOWING_PREFERENCE_AREA_ID_INDEX,
    MOWING_PREFERENCE_VERSION_INDEX,
)
from dreame.types import MowingPreferenceMode


def make_device() -> DreameMowerDevice:
    device = object.__new__(DreameMowerDevice)
    device.info = SimpleNamespace(model="dreame.mower.g2422")
    device.status = SimpleNamespace(
        cutting_height=None,
        zone_cutting_heights={},
        attributes={},
    )
    device._update_callback = Mock()
    device._protocol = SimpleNamespace(action=Mock(return_value={"code": 0}))
    device.schedule_update = Mock()
    return device


def test_refresh_cutting_height_success():
    device = make_device()
    fake_record = [0, 0, 0, 0, 45, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    device._protocol.action.return_value = {
        "code": 0,
        "out": [{"r": 0, "d": fake_record}],
    }

    result = device.refresh_cutting_height(map_id=1)

    assert result == 4.5
    assert device.status.cutting_height == 4.5
    device._protocol.action.assert_any_call(
        2,
        50,
        [{"m": "g", "t": "PRE", "d": {"idx": 0, "region": MOWING_PREFERENCE_GLOBAL_AREA_ID}}],
    )
    device._update_callback.assert_called()


def test_set_cutting_height_success():
    device = make_device()
    initial_record = [0, 0, 0, 0, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    device._protocol.action.side_effect = [
        {"code": 0, "out": [{"r": 0, "d": initial_record}]},  # Read base record
        {"code": 0, "out": [{"r": 0, "d": []}]},              # Write updated record
    ]

    result = device.set_cutting_height(5.5, map_id=1)

    assert result is True
    assert device.status.cutting_height == 5.5

    expected_written_record = list(initial_record)
    expected_written_record[MOWING_PREFERENCE_CUTTING_HEIGHT_INDEX] = 55
    expected_written_record[MOWING_PREFERENCE_MAP_INDEX_INDEX] = 0
    expected_written_record[MOWING_PREFERENCE_AREA_ID_INDEX] = 0
    expected_written_record[MOWING_PREFERENCE_VERSION_INDEX] = 0

    assert device._protocol.action.call_count == 2
    device._protocol.action.assert_has_calls([
        call(2, 50, [{"m": "g", "t": "PRE", "d": {"idx": 0, "region": 0}}]),
        call(2, 50, [{"m": "s", "t": "PRE", "d": expected_written_record}]),
    ])
    device.schedule_update.assert_called_with(1, True)


def test_set_cutting_height_zone_specific():
    device = make_device()
    initial_record = [0, 0, 0, 0, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    device._protocol.action.side_effect = [
        {"code": 0, "out": [{"r": 0, "d": initial_record}]},  # Read zone record
        {"code": 0, "out": [{"r": 0, "d": []}]},              # Write updated zone record
        {"code": 0, "out": [{"r": 0, "d": []}]},              # Set PREP mode to PER_ZONE
    ]

    result = device.set_cutting_height(6.0, map_id=1, zone_id=2)

    assert result is True
    assert device.status.zone_cutting_heights[2] == 6.0

    expected_written_record = list(initial_record)
    expected_written_record[MOWING_PREFERENCE_CUTTING_HEIGHT_INDEX] = 60
    expected_written_record[MOWING_PREFERENCE_MAP_INDEX_INDEX] = 0
    expected_written_record[MOWING_PREFERENCE_AREA_ID_INDEX] = 2
    expected_written_record[MOWING_PREFERENCE_VERSION_INDEX] = 0

    assert device._protocol.action.call_count == 3
    device._protocol.action.assert_has_calls([
        call(2, 50, [{"m": "g", "t": "PRE", "d": {"idx": 0, "region": 2}}]),
        call(2, 50, [{"m": "s", "t": "PRE", "d": expected_written_record}]),
        call(2, 50, [{"m": "s", "t": "PREP", "d": {"idx": 0, "value": int(MowingPreferenceMode.PER_ZONE)}}]),
    ])


def test_cutting_height_validation_bounds():
    device = make_device()

    with pytest.raises(ValueError, match="between 3.0 cm and 7.0 cm"):
        device.set_cutting_height(2.5)

    with pytest.raises(ValueError, match="between 3.0 cm and 7.0 cm"):
        device.set_cutting_height(7.5)

    with pytest.raises(ValueError, match="must be a number"):
        device.set_cutting_height("invalid")


def test_cutting_height_step_normalization():
    assert DreameMowerDevice._normalize_cutting_height(3.2) == 3.0
    assert DreameMowerDevice._normalize_cutting_height(3.3) == 3.5
    assert DreameMowerDevice._normalize_cutting_height(4.75) == 5.0
