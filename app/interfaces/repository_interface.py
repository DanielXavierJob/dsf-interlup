from abc import ABC, abstractmethod


class RepositoryInterface(ABC):
    """
        Interface for repository classes providing CRUD operations.
    """
    @abstractmethod
    def get_all(self):
        """
            Retrieves all items.

            Returns:
            A list of items.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: int | str):
        """
            Retrieves an item by its ID.

            Parameters:
            - id (int | str): The ID of the item to retrieve.

            Returns:
            The item corresponding to the specified ID.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_name(self, name: str):
        """
            Retrieves an item by its name.

            Parameters:
            - name (str): The name of the item to retrieve.

            Returns:
            The item corresponding to the specified name.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_order(self, order: int):
        """
            Retrieves an item by its order.

            Parameters:
            - order (int): The order of the item to retrieve.

            Returns:
            The item corresponding to the specified order.
        """
        raise NotImplementedError

    @abstractmethod
    def create(self, item):
        """
            Creates a new item.

            Parameters:
            - item: The item to create.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, item):
        """
            Updates an existing item.

            Parameters:
            - item: The item to update.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: int | str):
        """
            Deletes an item by its ID.

            Parameters:
            - id (int | str): The ID of the item to delete.
        """
        raise NotImplementedError
