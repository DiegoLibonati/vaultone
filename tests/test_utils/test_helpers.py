import os
import sys
from unittest.mock import patch

from src.utils.helpers import resource_path


class TestResourcePath:
    def test_returns_string(self) -> None:
        result: str = resource_path(relative_path="assets/image.png")
        assert isinstance(result, str)

    def test_without_meipass_uses_cwd(self) -> None:
        result: str = resource_path(relative_path="assets/image.png")
        expected: str = os.path.join(os.path.abspath("."), "assets/image.png")
        assert result == expected

    def test_with_meipass_uses_meipass(self) -> None:
        with patch.object(sys, "_MEIPASS", "/fake/meipass", create=True):
            result: str = resource_path(relative_path="assets/image.png")
            expected: str = os.path.join("/fake/meipass", "assets/image.png")
            assert result == expected

    def test_empty_relative_path_returns_string(self) -> None:
        result: str = resource_path(relative_path="")
        assert isinstance(result, str)

    def test_result_ends_with_filename(self) -> None:
        result: str = resource_path(relative_path="images/mic.png")
        assert result.endswith("mic.png")

    def test_with_meipass_does_not_use_cwd(self) -> None:
        cwd: str = os.path.abspath(".")
        with patch.object(sys, "_MEIPASS", "/fake/meipass", create=True):
            result: str = resource_path(relative_path="assets/image.png")
            assert not result.startswith(cwd)
