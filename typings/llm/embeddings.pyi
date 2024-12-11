"""
This type stub file was generated by pyright.
"""

from .models import EmbeddingModel
from dataclasses import dataclass
from sqlite_utils import Database
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

@dataclass
class Entry:
    id: str
    score: Optional[float]
    content: Optional[str] = ...
    metadata: Optional[Dict[str, Any]] = ...


class Collection:
    class DoesNotExist(Exception):
        ...


    def __init__(self, name: str, db: Optional[Database] = ..., *, model: Optional[EmbeddingModel] = ..., model_id: Optional[str] = ..., create: bool = ...) -> None:
        """
        A collection of embeddings

        Returns the collection with the given name, creating it if it does not exist.

        If you set create=False a Collection.DoesNotExist exception will be raised if the
        collection does not already exist.

        Args:
            db (sqlite_utils.Database): Database to store the collection in
            name (str): Name of the collection
            model (llm.models.EmbeddingModel, optional): Embedding model to use
            model_id (str, optional): Alternatively, ID of the embedding model to use
            create (bool, optional): Whether to create the collection if it does not exist
        """
        ...

    def model(self) -> EmbeddingModel:
        "Return the embedding model used by this collection"
        ...

    def count(self) -> int:
        """
        Count the number of items in the collection.

        Returns:
            int: Number of items in the collection
        """
        ...

    def embed(self, id: str, value: Union[str, bytes], metadata: Optional[Dict[str, Any]] = ..., store: bool = ...) -> None:
        """
        Embed value and store it in the collection with a given ID.

        Args:
            id (str): ID for the value
            value (str or bytes): value to be embedded
            metadata (dict, optional): Metadata to be stored
            store (bool, optional): Whether to store the value in the content or content_blob column
        """
        ...

    def embed_multi(self, entries: Iterable[Tuple[str, Union[str, bytes]]], store: bool = ..., batch_size: int = ...) -> None:
        """
        Embed multiple texts and store them in the collection with given IDs.

        Args:
            entries (iterable): Iterable of (id: str, text: str) tuples
            store (bool, optional): Whether to store the text in the content column
            batch_size (int, optional): custom maximum batch size to use
        """
        ...

    def embed_multi_with_metadata(self, entries: Iterable[Tuple[str, Union[str, bytes], Optional[Dict[str, Any]]]], store: bool = ..., batch_size: int = ...) -> None:
        """
        Embed multiple values along with metadata and store them in the collection with given IDs.

        Args:
            entries (iterable): Iterable of (id: str, value: str or bytes, metadata: None or dict)
            store (bool, optional): Whether to store the value in the content or content_blob column
            batch_size (int, optional): custom maximum batch size to use
        """
        ...

    def similar_by_vector(self, vector: List[float], number: int = ..., skip_id: Optional[str] = ...) -> List[Entry]:
        """
        Find similar items in the collection by a given vector.

        Args:
            vector (list): Vector to search by
            number (int, optional): Number of similar items to return

        Returns:
            list: List of Entry objects
        """
        ...

    def similar_by_id(self, id: str, number: int = ...) -> List[Entry]:
        """
        Find similar items in the collection by a given ID.

        Args:
            id (str): ID to search by
            number (int, optional): Number of similar items to return

        Returns:
            list: List of Entry objects
        """
        ...

    def similar(self, value: Union[str, bytes], number: int = ...) -> List[Entry]:
        """
        Find similar items in the collection by a given value.

        Args:
            value (str or bytes): value to search by
            number (int, optional): Number of similar items to return

        Returns:
            list: List of Entry objects
        """
        ...

    @classmethod
    def exists(cls, db: Database, name: str) -> bool:
        """
        Does this collection exist in the database?

        Args:
            name (str): Name of the collection
        """
        ...

    def delete(self): # -> None:
        """
        Delete the collection and its embeddings from the database
        """
        ...

    @staticmethod
    def content_hash(input: Union[str, bytes]) -> bytes:
        "Hash content for deduplication. Override to change hashing behavior."
        ...