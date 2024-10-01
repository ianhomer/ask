from abc import abstractmethod


class Pipeline:
    @abstractmethod
    def run(self) -> None:
        pass
