from unittest.mock import MagicMock, patch

import pytest

from src.models.audio_model import AudioModel
from src.utils.dialogs import InternalDialogError, ValidationDialogError


@pytest.fixture
def audio_model() -> AudioModel:
    with patch("pyaudio.PyAudio") as mock_pyaudio_class:
        mock_pyaudio_class.return_value = MagicMock()
        model: AudioModel = AudioModel(chunk=1024, sample_format=8, channels=1, fs=44100)
        yield model


class TestAudioModelInit:
    def test_chunk_property(self, audio_model: AudioModel) -> None:
        assert audio_model.chunk == 1024

    def test_sample_format_property(self, audio_model: AudioModel) -> None:
        assert audio_model.sample_format == 8

    def test_channels_property(self, audio_model: AudioModel) -> None:
        assert audio_model.channels == 1

    def test_fs_property(self, audio_model: AudioModel) -> None:
        assert audio_model.fs == 44100

    def test_seconds_initial_value(self, audio_model: AudioModel) -> None:
        assert audio_model.seconds == 0

    def test_minutes_initial_value(self, audio_model: AudioModel) -> None:
        assert audio_model.minutes == 0

    def test_stream_initial_is_none(self, audio_model: AudioModel) -> None:
        assert audio_model.stream is None

    def test_frames_initial_is_empty(self, audio_model: AudioModel) -> None:
        assert audio_model.frames == []

    def test_end_audio_initial_is_false(self, audio_model: AudioModel) -> None:
        assert audio_model.end_audio is False

    def test_recording_thread_initial_is_none(self, audio_model: AudioModel) -> None:
        assert audio_model.recording_thread is None

    def test_timer_thread_initial_is_none(self, audio_model: AudioModel) -> None:
        assert audio_model.timer_thread is None

    def test_py_audio_is_initialized(self, audio_model: AudioModel) -> None:
        assert audio_model.py_audio is not None


class TestAudioModelStopRecord:
    def test_empty_filename_raises_validation_error(self, audio_model: AudioModel) -> None:
        with pytest.raises(ValidationDialogError):
            audio_model.stop_record(filename="")

    def test_whitespace_filename_raises_validation_error(self, audio_model: AudioModel) -> None:
        with pytest.raises(ValidationDialogError):
            audio_model.stop_record(filename="   ")

    def test_no_threads_raises_internal_error(self, audio_model: AudioModel) -> None:
        with pytest.raises(InternalDialogError):
            audio_model.stop_record(filename="valid_filename")

    def test_empty_filename_error_message(self, audio_model: AudioModel) -> None:
        with pytest.raises(ValidationDialogError) as exc_info:
            audio_model.stop_record(filename="")
        assert "valid name" in exc_info.value.message.lower() or len(exc_info.value.message) > 0

    def test_no_threads_error_message(self, audio_model: AudioModel) -> None:
        with pytest.raises(InternalDialogError) as exc_info:
            audio_model.stop_record(filename="valid_filename")
        assert len(exc_info.value.message) > 0


class TestAudioModelStr:
    def test_str_returns_string(self, audio_model: AudioModel) -> None:
        result: str = str(audio_model)
        assert isinstance(result, str)

    def test_str_contains_chunk(self, audio_model: AudioModel) -> None:
        result: str = str(audio_model)
        assert "Chunk: 1024" in result

    def test_str_contains_channels(self, audio_model: AudioModel) -> None:
        result: str = str(audio_model)
        assert "Channels: 1" in result

    def test_str_contains_fs(self, audio_model: AudioModel) -> None:
        result: str = str(audio_model)
        assert "Fs: 44100" in result

    def test_str_contains_seconds(self, audio_model: AudioModel) -> None:
        result: str = str(audio_model)
        assert "Seconds: 0" in result

    def test_str_contains_minutes(self, audio_model: AudioModel) -> None:
        result: str = str(audio_model)
        assert "Minutes: 0" in result
