"""
serializer -- Configuration serialization interfaces.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from labw_utils.commonutils import lwio
from labw_utils.typing_importer import Mapping
from labw_utils.typing_importer import Optional, Any

__all__ = (
    "SerializableInterface",
)


class SerializableInterface(ABC):
    """
    Something that can be saved or loaded to files.
    """

    @classmethod
    def load(cls, path_of_fd: lwio.PathOrFDType, **kwargs):
        """
        Load configuration from a file.

        :param path_of_fd: Filename or buffer to read from.
        :return: New instance of corresponding class.
        """
        raise NotImplementedError

    def save(self, path_of_fd: lwio.PathOrFDType, **kwargs) -> None:
        """
        Save the class contents with metadata.

        :param path_of_fd: Filename or buffer to write to.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def _dump_versions() -> Optional[Mapping[str, Any]]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def _dump_metadata() -> Optional[Mapping[str, Any]]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def _validate_versions(versions: Mapping[str, Any]) -> None:
        raise NotImplementedError
