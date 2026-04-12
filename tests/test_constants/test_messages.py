from src.constants.messages import (
    MESSAGE_ERROR_APP,
    MESSAGE_ERROR_AUDIO_NOT_STARTED,
    MESSAGE_NOT_FOUND_DIALOG_TYPE,
    MESSAGE_NOT_VALID_FILENAME,
    MESSAGE_NOT_VALID_FILENAME_SAVE,
)


class TestMessages:
    def test_message_error_app_is_string(self) -> None:
        assert isinstance(MESSAGE_ERROR_APP, str)

    def test_message_error_app_not_empty(self) -> None:
        assert len(MESSAGE_ERROR_APP) > 0

    def test_message_error_app_value(self) -> None:
        assert MESSAGE_ERROR_APP == "Internal error. Contact a developer."

    def test_message_error_audio_not_started_is_string(self) -> None:
        assert isinstance(MESSAGE_ERROR_AUDIO_NOT_STARTED, str)

    def test_message_error_audio_not_started_not_empty(self) -> None:
        assert len(MESSAGE_ERROR_AUDIO_NOT_STARTED) > 0

    def test_message_error_audio_not_started_value(self) -> None:
        assert MESSAGE_ERROR_AUDIO_NOT_STARTED == "You must start an audio to be able to stop it."

    def test_message_not_valid_filename_save_is_string(self) -> None:
        assert isinstance(MESSAGE_NOT_VALID_FILENAME_SAVE, str)

    def test_message_not_valid_filename_save_value(self) -> None:
        assert MESSAGE_NOT_VALID_FILENAME_SAVE == "You must enter a valid name to save the file."

    def test_message_not_valid_filename_is_string(self) -> None:
        assert isinstance(MESSAGE_NOT_VALID_FILENAME, str)

    def test_message_not_valid_filename_value(self) -> None:
        assert MESSAGE_NOT_VALID_FILENAME == "You must enter a valid filename."

    def test_message_not_found_dialog_type_is_string(self) -> None:
        assert isinstance(MESSAGE_NOT_FOUND_DIALOG_TYPE, str)

    def test_message_not_found_dialog_type_value(self) -> None:
        assert MESSAGE_NOT_FOUND_DIALOG_TYPE == "The type of dialog to display is not found."
