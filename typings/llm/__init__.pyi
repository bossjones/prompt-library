"""
This type stub file was generated by pyright.
"""

import click
import json
import os
import pathlib
import struct
from .hookspecs import hookimpl
from .errors import ModelError, NeedsKeyException
from .models import AsyncModel, AsyncResponse, Attachment, Conversation, EmbeddingModel, EmbeddingModelWithAliases, Model, ModelWithAliases, Options, Prompt, Response
from .embeddings import Collection
from .templates import Template
from .plugins import load_plugins, pm
from typing import Dict, List, Optional

__all__ = ["hookimpl", "get_async_model", "get_model", "get_key", "user_dir", "AsyncResponse", "Attachment", "Collection", "Conversation", "Model", "Options", "Prompt", "Response", "Template", "ModelError", "NeedsKeyException"]
DEFAULT_MODEL = ...
def get_plugins(all=...): # -> list[Any]:
    ...

def get_models_with_aliases() -> List[ModelWithAliases]:
    ...

def get_embedding_models_with_aliases() -> List[EmbeddingModelWithAliases]:
    ...

def get_embedding_models(): # -> list[Any]:
    ...

def get_embedding_model(name): # -> EmbeddingModel:
    ...

def get_embedding_model_aliases() -> Dict[str, EmbeddingModel]:
    ...

def get_async_model_aliases() -> Dict[str, AsyncModel]:
    ...

def get_model_aliases() -> Dict[str, Model]:
    ...

class UnknownModelError(KeyError):
    ...


def get_models() -> List[Model]:
    "Get all registered models"
    ...

def get_async_models() -> List[AsyncModel]:
    "Get all registered async models"
    ...

def get_async_model(name: Optional[str] = ...) -> AsyncModel:
    "Get an async model by name or alias"
    ...

def get_model(name: Optional[str] = ..., _skip_async: bool = ...) -> Model:
    "Get a model by name or alias"
    ...

def get_key(explicit_key: Optional[str], key_alias: str, env_var: Optional[str] = ...) -> Optional[str]:
    """
    Return an API key based on a hierarchy of potential sources.

    :param provided_key: A key provided by the user. This may be the key, or an alias of a key in keys.json.
    :param key_alias: The alias used to retrieve the key from the keys.json file.
    :param env_var: Name of the environment variable to check for the key.
    """
    ...

def load_keys(): # -> Any | dict[Any, Any]:
    ...

def user_dir(): # -> Path:
    ...

def set_alias(alias, model_id_or_alias): # -> None:
    """
    Set an alias to point to the specified model.
    """
    ...

def remove_alias(alias): # -> None:
    """
    Remove an alias.
    """
    ...

def encode(values): # -> bytes:
    ...

def decode(binary): # -> tuple[Any, ...]:
    ...

def cosine_similarity(a, b): # -> Any:
    ...

def get_default_model(filename=..., default=...): # -> str:
    ...

def set_default_model(model, filename=...): # -> None:
    ...

def get_default_embedding_model(): # -> str:
    ...

def set_default_embedding_model(model): # -> None:
    ...
