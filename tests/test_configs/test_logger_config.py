import logging

from src.configs.logger_config import setup_logger


class TestSetupLogger:
    def test_returns_logger_instance(self) -> None:
        logger: logging.Logger = setup_logger("test-logger-returns")
        assert isinstance(logger, logging.Logger)

    def test_logger_name(self) -> None:
        logger: logging.Logger = setup_logger("test-logger-name-check")
        assert logger.name == "test-logger-name-check"

    def test_default_name(self) -> None:
        logger: logging.Logger = setup_logger()
        assert logger.name == "tkinter-app"

    def test_logger_level_is_debug(self) -> None:
        logger: logging.Logger = setup_logger("test-logger-level-check")
        assert logger.level == logging.DEBUG

    def test_logger_has_at_least_one_handler(self) -> None:
        logger: logging.Logger = setup_logger("test-logger-handler-check")
        assert len(logger.handlers) >= 1

    def test_handler_is_stream_handler(self) -> None:
        logger: logging.Logger = setup_logger("test-logger-stream-check")
        assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)

    def test_no_duplicate_handlers_on_multiple_calls(self) -> None:
        name: str = "test-logger-no-duplicate"
        setup_logger(name)
        setup_logger(name)
        logger: logging.Logger = logging.getLogger(name)
        assert len(logger.handlers) == 1
