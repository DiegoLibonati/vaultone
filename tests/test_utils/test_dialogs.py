from tkinter import messagebox
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from src.constants.messages import MESSAGE_ERROR_APP, MESSAGE_NOT_FOUND_DIALOG_TYPE
from src.utils.dialogs import (
    AuthenticationDialogError,
    BaseDialog,
    BaseDialogError,
    BusinessDialogError,
    ConflictDialogError,
    DeprecatedDialogWarning,
    InternalDialogError,
    NotFoundDialogError,
    SuccessDialogInformation,
    ValidationDialogError,
)


class TestBaseDialog:
    def test_error_constant(self) -> None:
        assert BaseDialog.ERROR == "Error"

    def test_warning_constant(self) -> None:
        assert BaseDialog.WARNING == "Warning"

    def test_info_constant(self) -> None:
        assert BaseDialog.INFO == "Info"

    def test_default_dialog_type_is_error(self) -> None:
        dialog: BaseDialog = BaseDialog()
        assert dialog.dialog_type == BaseDialog.ERROR

    def test_default_message(self) -> None:
        dialog: BaseDialog = BaseDialog()
        assert dialog.message == MESSAGE_ERROR_APP

    def test_custom_message_overrides_default(self) -> None:
        dialog: BaseDialog = BaseDialog(message="custom error")
        assert dialog.message == "custom error"

    def test_none_message_keeps_default(self) -> None:
        dialog: BaseDialog = BaseDialog(message=None)
        assert dialog.message == MESSAGE_ERROR_APP

    def test_title_for_error(self) -> None:
        dialog: BaseDialog = BaseDialog()
        assert dialog.title == "Error"

    def test_to_dict_returns_dict(self) -> None:
        dialog: BaseDialog = BaseDialog()
        result: dict[str, Any] = dialog.to_dict()
        assert isinstance(result, dict)

    def test_to_dict_contains_dialog_type(self) -> None:
        dialog: BaseDialog = BaseDialog()
        result: dict[str, Any] = dialog.to_dict()
        assert result["dialog_type"] == BaseDialog.ERROR

    def test_to_dict_contains_title(self) -> None:
        dialog: BaseDialog = BaseDialog()
        result: dict[str, Any] = dialog.to_dict()
        assert result["title"] == "Error"

    def test_to_dict_contains_message(self) -> None:
        dialog: BaseDialog = BaseDialog(message="test")
        result: dict[str, Any] = dialog.to_dict()
        assert result["message"] == "test"

    def test_open_calls_handler(self) -> None:
        dialog: BaseDialog = BaseDialog(message="test error")
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.ERROR: mock_handler}):
            dialog.open()
            mock_handler.assert_called_once_with("Error", "test error")

    def test_open_unknown_type_calls_showerror(self) -> None:
        dialog: BaseDialog = BaseDialog()
        dialog.dialog_type = "UNKNOWN"  # type: ignore[assignment]
        with patch.object(messagebox, "showerror") as mock_showerror:
            dialog.open()
            mock_showerror.assert_called_once_with(BaseDialog.ERROR, MESSAGE_NOT_FOUND_DIALOG_TYPE)


class TestBaseDialogError:
    def test_is_exception(self) -> None:
        error: BaseDialogError = BaseDialogError()
        assert isinstance(error, Exception)

    def test_is_base_dialog(self) -> None:
        error: BaseDialogError = BaseDialogError()
        assert isinstance(error, BaseDialog)

    def test_dialog_type_is_error(self) -> None:
        error: BaseDialogError = BaseDialogError()
        assert error.dialog_type == BaseDialog.ERROR

    def test_default_message(self) -> None:
        error: BaseDialogError = BaseDialogError()
        assert error.message == MESSAGE_ERROR_APP


class TestValidationDialogError:
    def test_is_base_dialog_error(self) -> None:
        assert isinstance(ValidationDialogError(), BaseDialogError)

    def test_default_message(self) -> None:
        assert ValidationDialogError().message == "Validation error"

    def test_custom_message(self) -> None:
        error: ValidationDialogError = ValidationDialogError(message="custom validation")
        assert error.message == "custom validation"

    def test_can_be_raised_and_caught(self) -> None:
        with pytest.raises(ValidationDialogError):
            raise ValidationDialogError(message="test")

    def test_dialog_type_is_error(self) -> None:
        assert ValidationDialogError().dialog_type == BaseDialog.ERROR


class TestInternalDialogError:
    def test_is_base_dialog_error(self) -> None:
        assert isinstance(InternalDialogError(), BaseDialogError)

    def test_default_message(self) -> None:
        assert InternalDialogError().message == "Internal error"

    def test_custom_message(self) -> None:
        error: InternalDialogError = InternalDialogError(message="custom internal")
        assert error.message == "custom internal"

    def test_can_be_raised_and_caught(self) -> None:
        with pytest.raises(InternalDialogError):
            raise InternalDialogError(message="test")


class TestAuthenticationDialogError:
    def test_is_base_dialog_error(self) -> None:
        assert isinstance(AuthenticationDialogError(), BaseDialogError)

    def test_default_message(self) -> None:
        assert AuthenticationDialogError().message == "Authentication error"


class TestNotFoundDialogError:
    def test_is_base_dialog_error(self) -> None:
        assert isinstance(NotFoundDialogError(), BaseDialogError)

    def test_default_message(self) -> None:
        assert NotFoundDialogError().message == "Resource not found"


class TestConflictDialogError:
    def test_is_base_dialog_error(self) -> None:
        assert isinstance(ConflictDialogError(), BaseDialogError)

    def test_default_message(self) -> None:
        assert ConflictDialogError().message == "Conflict error"


class TestBusinessDialogError:
    def test_is_base_dialog_error(self) -> None:
        assert isinstance(BusinessDialogError(), BaseDialogError)

    def test_default_message(self) -> None:
        assert BusinessDialogError().message == "Business rule violated"


class TestDeprecatedDialogWarning:
    def test_dialog_type_is_warning(self) -> None:
        warning: DeprecatedDialogWarning = DeprecatedDialogWarning()
        assert warning.dialog_type == BaseDialog.WARNING

    def test_default_message(self) -> None:
        assert DeprecatedDialogWarning().message == "This feature is deprecated"

    def test_title_is_warning(self) -> None:
        assert DeprecatedDialogWarning().title == "Warning"

    def test_open_calls_showwarning(self) -> None:
        warning: DeprecatedDialogWarning = DeprecatedDialogWarning()
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.WARNING: mock_handler}):
            warning.open()
            mock_handler.assert_called_once_with("Warning", "This feature is deprecated")


class TestSuccessDialogInformation:
    def test_dialog_type_is_info(self) -> None:
        info: SuccessDialogInformation = SuccessDialogInformation()
        assert info.dialog_type == BaseDialog.INFO

    def test_default_message(self) -> None:
        assert SuccessDialogInformation().message == "Operation completed successfully"

    def test_title_is_information(self) -> None:
        assert SuccessDialogInformation().title == "Information"

    def test_open_calls_showinfo(self) -> None:
        info: SuccessDialogInformation = SuccessDialogInformation()
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.INFO: mock_handler}):
            info.open()
            mock_handler.assert_called_once_with("Information", "Operation completed successfully")
