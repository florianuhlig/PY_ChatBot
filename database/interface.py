from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any


class DatabaseInterface(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def create_user_table(self) -> None:
        pass

    @abstractmethod
    def create_user(self, username: str, email: str, password_hash: str) -> bool:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_password_hash_by_email(self, email: str) -> Optional[str]:
        pass

    @abstractmethod
    def update_user_password(self, email: str, new_password_hash: str) -> bool:
        pass

    @abstractmethod
    def delete_user(self, email: str) -> bool:
        pass
