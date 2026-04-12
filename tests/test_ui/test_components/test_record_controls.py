import tkinter as tk
from collections.abc import Generator
from tkinter import DISABLED, NORMAL

import pytest

from src.ui.components.record_controls import RecordControls
from src.ui.styles import Styles


@pytest.fixture
def record_controls(root: tk.Tk) -> Generator[RecordControls, None, None]:
    controls: RecordControls = RecordControls(
        parent=root,
        styles=Styles(),
        on_start=lambda: None,
        on_stop=lambda: None,
    )
    yield controls
    controls.destroy()


class TestRecordControlsInit:
    def test_instantiation(self, root: tk.Tk) -> None:
        controls: RecordControls = RecordControls(
            parent=root,
            styles=Styles(),
            on_start=lambda: None,
            on_stop=lambda: None,
        )
        assert controls is not None
        controls.destroy()

    def test_initial_filename_is_empty(self, record_controls: RecordControls) -> None:
        assert record_controls.get_filename() == ""

    def test_start_button_initial_state_is_normal(self, record_controls: RecordControls) -> None:
        assert str(record_controls._start_button["state"]) == NORMAL

    def test_stop_button_initial_state_is_disabled(self, record_controls: RecordControls) -> None:
        assert str(record_controls._stop_button["state"]) == DISABLED

    def test_is_recording_initial_value_is_false(self, record_controls: RecordControls) -> None:
        assert record_controls.is_recording() is False


class TestRecordControlsFilename:
    def test_set_filename(self, record_controls: RecordControls) -> None:
        record_controls.set_filename("my_audio")
        assert record_controls.get_filename() == "my_audio"

    def test_set_filename_empty(self, record_controls: RecordControls) -> None:
        record_controls.set_filename("")
        assert record_controls.get_filename() == ""

    def test_set_filename_with_spaces(self, record_controls: RecordControls) -> None:
        record_controls.set_filename("audio file name")
        assert record_controls.get_filename() == "audio file name"

    def test_set_filename_overwrites_previous(self, record_controls: RecordControls) -> None:
        record_controls.set_filename("first")
        record_controls.set_filename("second")
        assert record_controls.get_filename() == "second"


class TestRecordControlsRecordingState:
    def test_set_recording_true_disables_start(self, record_controls: RecordControls) -> None:
        record_controls.set_recording_state(recording=True)
        assert str(record_controls._start_button["state"]) == DISABLED

    def test_set_recording_true_enables_stop(self, record_controls: RecordControls) -> None:
        record_controls.set_recording_state(recording=True)
        assert str(record_controls._stop_button["state"]) == NORMAL

    def test_set_recording_false_enables_start(self, record_controls: RecordControls) -> None:
        record_controls.set_recording_state(recording=True)
        record_controls.set_recording_state(recording=False)
        assert str(record_controls._start_button["state"]) == NORMAL

    def test_set_recording_false_disables_stop(self, record_controls: RecordControls) -> None:
        record_controls.set_recording_state(recording=True)
        record_controls.set_recording_state(recording=False)
        assert str(record_controls._stop_button["state"]) == DISABLED

    def test_is_recording_true_when_stop_enabled(self, record_controls: RecordControls) -> None:
        record_controls.set_recording_state(recording=True)
        assert record_controls.is_recording() is True

    def test_is_recording_false_when_stop_disabled(self, record_controls: RecordControls) -> None:
        record_controls.set_recording_state(recording=False)
        assert record_controls.is_recording() is False
