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


class TestAudioModelStartRecord:
    def test_opens_stream_with_correct_params(self) -> None:
        with (
            patch("pyaudio.PyAudio") as mock_pyaudio_class,
            patch("src.models.audio_model.threading.Thread") as mock_thread_cls,
        ):
            mock_py_audio: MagicMock = MagicMock()
            mock_stream: MagicMock = MagicMock()
            mock_pyaudio_class.return_value = mock_py_audio
            mock_py_audio.open.return_value = mock_stream
            mock_thread_cls.return_value = MagicMock()

            model: AudioModel = AudioModel(chunk=1024, sample_format=8, channels=1, fs=44100)
            model.start_record()

        mock_py_audio.open.assert_called_once_with(
            format=8,
            channels=1,
            rate=44100,
            frames_per_buffer=1024,
            input=True,
        )

    def test_assigns_stream_after_open(self) -> None:
        with (
            patch("pyaudio.PyAudio") as mock_pyaudio_class,
            patch("src.models.audio_model.threading.Thread") as mock_thread_cls,
        ):
            mock_py_audio: MagicMock = MagicMock()
            mock_stream: MagicMock = MagicMock()
            mock_pyaudio_class.return_value = mock_py_audio
            mock_py_audio.open.return_value = mock_stream
            mock_thread_cls.return_value = MagicMock()

            model: AudioModel = AudioModel(chunk=1024, sample_format=8, channels=1, fs=44100)
            model.start_record()

        assert model.stream is mock_stream

    def test_starts_two_threads(self) -> None:
        with (
            patch("pyaudio.PyAudio") as mock_pyaudio_class,
            patch("src.models.audio_model.threading.Thread") as mock_thread_cls,
        ):
            mock_pyaudio_class.return_value = MagicMock()
            mock_thread: MagicMock = MagicMock()
            mock_thread_cls.return_value = mock_thread

            model: AudioModel = AudioModel(chunk=1024, sample_format=8, channels=1, fs=44100)
            model.start_record()

        assert mock_thread.start.call_count == 2

    def test_assigns_recording_and_timer_threads(self) -> None:
        with (
            patch("pyaudio.PyAudio") as mock_pyaudio_class,
            patch("src.models.audio_model.threading.Thread") as mock_thread_cls,
        ):
            mock_pyaudio_class.return_value = MagicMock()
            mock_thread: MagicMock = MagicMock()
            mock_thread_cls.return_value = mock_thread

            model: AudioModel = AudioModel(chunk=1024, sample_format=8, channels=1, fs=44100)
            model.start_record()

        assert model.recording_thread is mock_thread
        assert model.timer_thread is mock_thread


class TestAudioModelStopRecordSuccess:
    def test_returns_true_on_success(self, audio_model: AudioModel) -> None:
        mock_thread: MagicMock = MagicMock()
        mock_stream: MagicMock = MagicMock()
        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread
        audio_model._AudioModel__stream = mock_stream
        audio_model.py_audio.get_sample_size.return_value = 2

        with patch("src.models.audio_model.wave.open") as mock_wave_open:
            mock_wave_open.return_value = MagicMock()
            result: bool = audio_model.stop_record(filename="recording")

        assert result is True

    def test_writes_wav_with_correct_filename(self, audio_model: AudioModel) -> None:
        mock_thread: MagicMock = MagicMock()
        mock_stream: MagicMock = MagicMock()
        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread
        audio_model._AudioModel__stream = mock_stream
        audio_model.py_audio.get_sample_size.return_value = 2

        with patch("src.models.audio_model.wave.open") as mock_wave_open:
            mock_wave_file: MagicMock = MagicMock()
            mock_wave_open.return_value = mock_wave_file
            audio_model.stop_record(filename="my_audio")

        mock_wave_open.assert_called_once_with("my_audio.wav", "wb")

    def test_wav_configured_with_correct_channels_and_rate(self, audio_model: AudioModel) -> None:
        mock_thread: MagicMock = MagicMock()
        mock_stream: MagicMock = MagicMock()
        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread
        audio_model._AudioModel__stream = mock_stream
        audio_model.py_audio.get_sample_size.return_value = 2

        with patch("src.models.audio_model.wave.open") as mock_wave_open:
            mock_wave_file: MagicMock = MagicMock()
            mock_wave_open.return_value = mock_wave_file
            audio_model.stop_record(filename="test")

        mock_wave_file.setnchannels.assert_called_once_with(1)
        mock_wave_file.setframerate.assert_called_once_with(44100)

    def test_resets_timer_state_after_success(self, audio_model: AudioModel) -> None:
        mock_thread: MagicMock = MagicMock()
        mock_stream: MagicMock = MagicMock()
        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread
        audio_model._AudioModel__stream = mock_stream
        audio_model._AudioModel__seconds = 42
        audio_model._AudioModel__minutes = 3
        audio_model.py_audio.get_sample_size.return_value = 2

        with patch("src.models.audio_model.wave.open"):
            audio_model.stop_record(filename="test")

        assert audio_model.seconds == 0
        assert audio_model.minutes == 0

    def test_resets_recording_state_after_success(self, audio_model: AudioModel) -> None:
        mock_thread: MagicMock = MagicMock()
        mock_stream: MagicMock = MagicMock()
        audio_model._AudioModel__recording_thread = mock_thread
        audio_model._AudioModel__timer_thread = mock_thread
        audio_model._AudioModel__stream = mock_stream
        audio_model.py_audio.get_sample_size.return_value = 2

        with patch("src.models.audio_model.wave.open"):
            audio_model.stop_record(filename="test")

        assert audio_model.end_audio is False
        assert audio_model.recording_thread is None
        assert audio_model.timer_thread is None
        assert audio_model.stream is None
        assert audio_model.frames == []


class TestAudioModelRunTimer:
    def test_does_nothing_when_end_audio_is_true(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__end_audio = True

        audio_model._run_timer()

        assert audio_model.seconds == 0
        assert audio_model.minutes == 0


class TestAudioModelResetState:
    def test_clears_seconds_and_minutes(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__seconds = 45
        audio_model._AudioModel__minutes = 2
        audio_model._AudioModel__stream = None

        audio_model._reset_state()

        assert audio_model.seconds == 0
        assert audio_model.minutes == 0

    def test_clears_frames(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__frames = [b"data1", b"data2"]
        audio_model._AudioModel__stream = None

        audio_model._reset_state()

        assert audio_model.frames == []

    def test_clears_end_audio_flag(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__end_audio = True
        audio_model._AudioModel__stream = None

        audio_model._reset_state()

        assert audio_model.end_audio is False

    def test_clears_thread_references(self, audio_model: AudioModel) -> None:
        audio_model._AudioModel__stream = None

        audio_model._reset_state()

        assert audio_model.recording_thread is None
        assert audio_model.timer_thread is None

    def test_clears_stream_reference(self, audio_model: AudioModel) -> None:
        mock_stream: MagicMock = MagicMock()
        audio_model._AudioModel__stream = mock_stream

        audio_model._reset_state()

        assert audio_model.stream is None

    def test_calls_stop_stream_and_close_when_stream_exists(self, audio_model: AudioModel) -> None:
        mock_stream: MagicMock = MagicMock()
        audio_model._AudioModel__stream = mock_stream

        audio_model._reset_state()

        mock_stream.stop_stream.assert_called_once()
        mock_stream.close.assert_called_once()
