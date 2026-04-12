from src.constants.paths import PATH_MIC, PATH_MIC_ON


class TestPaths:
    def test_path_mic_is_string(self) -> None:
        assert isinstance(PATH_MIC, str)

    def test_path_mic_on_is_string(self) -> None:
        assert isinstance(PATH_MIC_ON, str)

    def test_path_mic_ends_with_png(self) -> None:
        assert PATH_MIC.endswith(".png")

    def test_path_mic_on_ends_with_png(self) -> None:
        assert PATH_MIC_ON.endswith(".png")

    def test_path_mic_contains_mic(self) -> None:
        assert "mic" in PATH_MIC.lower()

    def test_path_mic_on_contains_micon(self) -> None:
        assert "micon" in PATH_MIC_ON.lower()

    def test_paths_are_different(self) -> None:
        assert PATH_MIC != PATH_MIC_ON
