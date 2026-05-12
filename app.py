import os
from tkinter import Tk

from dotenv import load_dotenv
from pyaudio import paInt16

from src.configs.development_config import DevelopmentConfig
from src.configs.logger_config import setup_logger
from src.configs.production_config import ProductionConfig
from src.configs.testing_config import TestingConfig
from src.models.audio_model import AudioModel
from src.ui.interface_app import InterfaceApp
from src.utils.tkinter_exception_hook import tkinter_exception_hook

CONFIG_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def main(environment: str = "production") -> None:
    logger = setup_logger("vaultone - app.py")
    load_dotenv()

    environment = os.getenv("ENVIRONMENT", environment)

    root = Tk()
    root.report_callback_exception = tkinter_exception_hook

    config_class = CONFIG_MAP.get(environment, ProductionConfig)
    config = config_class()
    audio = AudioModel(chunk=1024, sample_format=paInt16, channels=1, fs=44100)

    interface_app = InterfaceApp(root=root, audio=audio, config=config)
    root.mainloop()

    logger.info("App finished: %s", interface_app)


if __name__ == "__main__":
    main(environment="development")
