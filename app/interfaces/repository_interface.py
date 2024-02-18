from abc import ABC, abstractmethod


class RepositoryInterface(ABC):
    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: int | str):
        raise NotImplementedError

    @abstractmethod
    def get_by_name(self, name: str):
        raise NotImplementedError

    @abstractmethod
    def get_by_order(self, order: int):
        raise NotImplementedError

    @abstractmethod
    def create(self, item):
        raise NotImplementedError

    @abstractmethod
    def update(self, item):
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: int | str):
        raise NotImplementedError
