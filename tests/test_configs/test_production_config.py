from src.configs.default_config import DefaultConfig
from src.configs.production_config import ProductionConfig


class TestProductionConfig:
    def test_debug_is_false(self) -> None:
        config: ProductionConfig = ProductionConfig()
        assert config.DEBUG is False

    def test_env_is_production(self) -> None:
        config: ProductionConfig = ProductionConfig()
        assert config.ENV == "production"

    def test_testing_is_false(self) -> None:
        config: ProductionConfig = ProductionConfig()
        assert config.TESTING is False

    def test_inherits_default_config(self) -> None:
        config: ProductionConfig = ProductionConfig()
        assert isinstance(config, DefaultConfig)

    def test_has_tz_attribute(self) -> None:
        config: ProductionConfig = ProductionConfig()
        assert hasattr(config, "TZ")

    def test_has_env_name_attribute(self) -> None:
        config: ProductionConfig = ProductionConfig()
        assert hasattr(config, "ENV_NAME")
