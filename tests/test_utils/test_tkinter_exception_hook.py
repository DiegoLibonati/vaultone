from unittest.mock import MagicMock, patch

from src.utils.dialogs import InternalDialogError, ValidationDialogError
from src.utils.tkinter_exception_hook import tkinter_exception_hook


class TestTkinterExceptionHook:
    def test_base_dialog_calls_open(self) -> None:
        exc: ValidationDialogError = ValidationDialogError(message="test")
        exc.open = MagicMock()

        tkinter_exception_hook(type(exc), exc, None)

        exc.open.assert_called_once()

    def test_internal_dialog_calls_open(self) -> None:
        exc: InternalDialogError = InternalDialogError(message="internal")
        exc.open = MagicMock()

        tkinter_exception_hook(type(exc), exc, None)

        exc.open.assert_called_once()

    def test_non_dialog_exception_creates_internal_error(self) -> None:
        exc: RuntimeError = RuntimeError("unexpected error")

        with patch("src.utils.tkinter_exception_hook.InternalDialogError") as mock_class:
            mock_instance: MagicMock = MagicMock()
            mock_class.return_value = mock_instance
            tkinter_exception_hook(type(exc), exc, None)

        mock_class.assert_called_once_with(message="unexpected error")
        mock_instance.open.assert_called_once()

    def test_non_dialog_exception_message_is_passed(self) -> None:
        exc: ValueError = ValueError("bad value")

        with patch("src.utils.tkinter_exception_hook.InternalDialogError") as mock_class:
            mock_instance: MagicMock = MagicMock()
            mock_class.return_value = mock_instance
            tkinter_exception_hook(type(exc), exc, None)

        mock_class.assert_called_once_with(message="bad value")

    # def test_logs_error_for_any_exception(self) -> None:
    #     exc: RuntimeError = RuntimeError("boom")

    #     with (
    #         patch("src.utils.tkinter_exception_hook.logger") as mock_logger,
    #         patch("src.utils.tkinter_exception_hook.InternalDialogError"),
    #     ):
    #         tkinter_exception_hook(type(exc), exc, None)

    #     mock_logger.error.assert_called_once()

    def test_exception_with_none_traceback_is_handled(self) -> None:
        exc: ValidationDialogError = ValidationDialogError(message="no tb")
        exc.open = MagicMock()

        tkinter_exception_hook(ValidationDialogError, exc, None)

        exc.open.assert_called_once()
