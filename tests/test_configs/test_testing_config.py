from src.configs.default_config import DefaultConfig
from src.configs.testing_config import TestingConfig


class TestTestingConfig:
    def test_testing_is_true(self) -> None:
        config: TestingConfig = TestingConfig()
        assert config.TESTING is True

    def test_debug_is_true(self) -> None:
        config: TestingConfig = TestingConfig()
        assert config.DEBUG is True

    def test_env_is_testing(self) -> None:
        config: TestingConfig = TestingConfig()
        assert config.ENV == "testing"

    def test_inherits_default_config(self) -> None:
        config: TestingConfig = TestingConfig()
        assert isinstance(config, DefaultConfig)

    def test_has_tz_attribute(self) -> None:
        config: TestingConfig = TestingConfig()
        assert hasattr(config, "TZ")

    def test_has_env_name_attribute(self) -> None:
        config: TestingConfig = TestingConfig()
        assert hasattr(config, "ENV_NAME")
