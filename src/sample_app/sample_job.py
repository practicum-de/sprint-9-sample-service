import time
from datetime import datetime
from logging import Logger


class SampleMessageProcessor:
    def __init__(self,
                 logger: Logger) -> None:
        self._logger = logger

    def run(self) -> None:
        self._logger.info(f"{datetime.utcnow()}: START")

        # imitation of some work.
        time.sleep(2.5)

        self._logger.info(f"{datetime.utcnow()}: FINISH")
