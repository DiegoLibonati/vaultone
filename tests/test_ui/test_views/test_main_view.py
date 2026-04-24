import tkinter as tk

import pytest

from src.ui.styles import Styles
from src.ui.views.main_view import MainView


@pytest.fixture
def blank_image(root: tk.Tk) -> tk.PhotoImage:
    return tk.PhotoImage(master=root, width=1, height=1)


@pytest.fixture
def main_view(root: tk.Tk, blank_image: tk.PhotoImage) -> MainView:
    view: MainView = MainView(
        root=root,
        styles=Styles(),
        img_record_off=blank_image,
        img_record_on=blank_image,
        on_start=lambda: None,
        on_stop=lambda: None,
    )
    yield view
    view.destroy()


class TestMainViewInit:
    def test_instantiation(self, root: tk.Tk, blank_image: tk.PhotoImage) -> None:
        view: MainView = MainView(
            root=root,
            styles=Styles(),
            img_record_off=blank_image,
            img_record_on=blank_image,
            on_start=lambda: None,
            on_stop=lambda: None,
        )
        assert view is not None
        view.destroy()

    def test_initial_status_text(self, main_view: MainView) -> None:
        assert main_view._status_text.get() == "Starts"

    def test_initial_is_recording_false(self, main_view: MainView) -> None:
        assert main_view.is_recording() is False

    def test_initial_filename_is_empty(self, main_view: MainView) -> None:
        assert main_view.get_filename() == ""


class TestMainViewFilename:
    def test_set_filename(self, main_view: MainView) -> None:
        main_view.set_filename("test_file")
        assert main_view.get_filename() == "test_file"

    def test_set_filename_empty(self, main_view: MainView) -> None:
        main_view.set_filename("")
        assert main_view.get_filename() == ""

    def test_set_filename_overwrites_previous(self, main_view: MainView) -> None:
        main_view.set_filename("first")
        main_view.set_filename("second")
        assert main_view.get_filename() == "second"


class TestMainViewStatus:
    def test_set_status(self, main_view: MainView) -> None:
        main_view.set_status("Recording...")
        assert main_view._status_text.get() == "Recording..."

    def test_set_status_empty(self, main_view: MainView) -> None:
        main_view.set_status("")
        assert main_view._status_text.get() == ""

    def test_set_status_overwrites(self, main_view: MainView) -> None:
        main_view.set_status("first")
        main_view.set_status("second")
        assert main_view._status_text.get() == "second"


class TestMainViewRecordingState:
    def test_set_recording_state_true(self, main_view: MainView) -> None:
        main_view.set_recording_state(recording=True)
        assert main_view.is_recording() is True

    def test_set_recording_state_false(self, main_view: MainView) -> None:
        main_view.set_recording_state(recording=True)
        main_view.set_recording_state(recording=False)
        assert main_view.is_recording() is False

    def test_recording_state_affects_filename_controls(self, main_view: MainView) -> None:
        main_view.set_filename("test")
        main_view.set_recording_state(recording=True)
        assert main_view.get_filename() == "test"
