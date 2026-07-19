from abc import ABC, abstractmethod

class BaseRetriever(ABC):
    @abstractmethod
    def retrieve(self, query: str, n_results: int=3) ->str:

        pass

