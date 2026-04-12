from unittest.mock import MagicMock, patch

from src.utils.dialogs import InternalDialogError, ValidationDialogError
from src.utils.error_handler import error_handler


class TestErrorHandler:
    def test_base_dialog_calls_open(self) -> None:
        exc: ValidationDialogError = ValidationDialogError(message="test")
        exc.open = MagicMock()  # type: ignore[method-assign]
        error_handler(type(exc), exc, None)
        exc.open.assert_called_once()

    def test_internal_dialog_calls_open(self) -> None:
        exc: InternalDialogError = InternalDialogError(message="internal")
        exc.open = MagicMock()  # type: ignore[method-assign]
        error_handler(type(exc), exc, None)
        exc.open.assert_called_once()

    def test_non_dialog_exception_creates_internal_error(self) -> None:
        exc: RuntimeError = RuntimeError("unexpected error")
        with patch("src.utils.error_handler.InternalDialogError") as mock_class:
            mock_instance: MagicMock = MagicMock()
            mock_class.return_value = mock_instance
            error_handler(type(exc), exc, None)
            mock_class.assert_called_once_with(message="unexpected error")
            mock_instance.open.assert_called_once()

    def test_non_dialog_exception_message_is_passed(self) -> None:
        exc: ValueError = ValueError("bad value")
        with patch("src.utils.error_handler.InternalDialogError") as mock_class:
            mock_instance: MagicMock = MagicMock()
            mock_class.return_value = mock_instance
            error_handler(type(exc), exc, None)
            mock_class.assert_called_once_with(message="bad value")

    def test_exception_with_none_traceback_is_handled(self) -> None:
        exc: ValidationDialogError = ValidationDialogError(message="no tb")
        exc.open = MagicMock()  # type: ignore[method-assign]
        error_handler(ValidationDialogError, exc, None)
        exc.open.assert_called_once()
