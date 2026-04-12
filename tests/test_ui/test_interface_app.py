import tkinter as tk
from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from src.configs.default_config import DefaultConfig
from src.models.audio_model import AudioModel
from src.ui.interface_app import InterfaceApp
from src.utils.dialogs import ValidationDialogError


@pytest.fixture
def mock_audio() -> MagicMock:
    audio: MagicMock = MagicMock(spec=AudioModel)
    audio.seconds = 0
    audio.minutes = 0
    audio.end_audio = False
    return audio


@pytest.fixture
def interface_app(root: tk.Tk, mock_audio: MagicMock) -> Generator[InterfaceApp, None, None]:
    blank: tk.PhotoImage = tk.PhotoImage(master=root, width=1, height=1)
    with patch("src.ui.interface_app.PhotoImage", return_value=blank):
        app: InterfaceApp = InterfaceApp(
            root=root,
            audio=mock_audio,
            config=DefaultConfig(),
        )
        yield app
        app._main_view.destroy()


class TestInterfaceAppInit:
    def test_instantiation(self, interface_app: InterfaceApp) -> None:
        assert interface_app is not None

    def test_audio_property(self, interface_app: InterfaceApp, mock_audio: MagicMock) -> None:
        assert interface_app.audio is mock_audio


class TestInterfaceAppParseTimer:
    def test_both_under_10(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=5, minutes=3)
        assert result == "03:05"

    def test_seconds_under_10_minutes_gte_10(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=5, minutes=10)
        assert result == "10:05"

    def test_seconds_gte_10_minutes_under_10(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=15, minutes=3)
        assert result == "03:15"

    def test_both_gte_10(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=15, minutes=10)
        assert result == "10:15"

    def test_zero_zero(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=0, minutes=0)
        assert result == "00:00"

    def test_boundary_seconds_9(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=9, minutes=0)
        assert result == "00:09"

    def test_boundary_seconds_10(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=10, minutes=0)
        assert result == "00:10"

    def test_boundary_minutes_9(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=0, minutes=9)
        assert result == "09:00"

    def test_boundary_minutes_10(self) -> None:
        result: str = InterfaceApp._parse_timer(seconds=0, minutes=10)
        assert result == "10:00"


class TestInterfaceAppPerformStartRecord:
    def test_empty_filename_raises_validation_error(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.set_filename("")
        with pytest.raises(ValidationDialogError):
            interface_app._perform_start_record()

    def test_valid_filename_calls_audio_start_record(self, interface_app: InterfaceApp, mock_audio: MagicMock) -> None:
        interface_app._main_view.set_filename("my_audio")
        interface_app._perform_start_record()
        mock_audio.start_record.assert_called_once()

    def test_valid_filename_sets_recording_state(self, interface_app: InterfaceApp, mock_audio: MagicMock) -> None:
        interface_app._main_view.set_filename("my_audio")
        interface_app._perform_start_record()
        assert interface_app._main_view.is_recording() is True


class TestInterfaceAppPerformStopRecord:
    def test_stop_record_calls_audio_stop_record(self, interface_app: InterfaceApp, mock_audio: MagicMock) -> None:
        mock_audio.stop_record.return_value = True
        interface_app._main_view.set_filename("my_audio")
        interface_app._perform_stop_record()
        mock_audio.stop_record.assert_called_once_with(filename="my_audio")

    def test_stop_record_sets_not_recording(self, interface_app: InterfaceApp, mock_audio: MagicMock) -> None:
        mock_audio.stop_record.return_value = True
        interface_app._main_view.set_recording_state(recording=True)
        interface_app._perform_stop_record()
        assert interface_app._main_view.is_recording() is False
