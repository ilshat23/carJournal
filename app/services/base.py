from abc import ABC, abstractmethod


class BaseService(ABC):
    @abstractmethod
    async def register_user(self, **kwargs):
        pass
