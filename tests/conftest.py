# pylint: disable=no-member
# pylint: disable=no-member
# pylint: disable=possibly-used-before-assignment
# pyright: reportImportCycles=false
# pyright: reportUndefinedVariable=false
# pyright: reportAttributeAccessIssue=false
# pyright: reportInvalidTypeForm=false
# mypy: disable-error-code="index"
# mypy: disable-error-code="no-redef"
"""Global test fixtures definitions."""

from __future__ import annotations

import copy
import datetime
import functools
import glob
import os
import posixpath
import re
import shutil
import sys

from collections.abc import Generator, Iterable, Iterator
from concurrent.futures import Executor, Future
from dataclasses import dataclass
from http import client
from pathlib import Path, PosixPath
from typing import TYPE_CHECKING, Any, Optional, TypeVar, Union

from _pytest.logging import LogCaptureFixture
from _pytest.monkeypatch import MonkeyPatch
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings
from rich.console import Console
from rich.markdown import Markdown
from vcr import filters

import pytest


if TYPE_CHECKING:
    from _pytest.config import Config as PytestConfig
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch
    from vcr.config import VCR
    from vcr.request import Request as VCRRequest

    from pytest_mock.plugin import MockerFixture

INDEX_NAME = "goobaiunittest"

T = TypeVar("T")

YieldFixture = Generator[T, None, None]


IS_RUNNING_ON_GITHUB_ACTIONS = bool(os.environ.get("GITHUB_ACTOR"))

HERE = os.path.abspath(os.path.dirname(__file__))
FAKE_TIME = datetime.datetime(2020, 12, 25, 17, 5, 55)


class IgnoreOrder:
    """
    pytest helper to test equality of lists/tuples ignoring item order.

    E.g., these asserts pass:
    >>> assert [1, 2, 3, 3] == IgnoreOrder([3, 1, 2, 3])
    >>> assert {"foo": [1, 2, 3]} == {"foo": IgnoreOrder([3, 2, 1])}
    """

    def __init__(self, items: list | tuple, key: Any | None = None) -> None:
        self.items = items
        self.key = key

    def __eq__(self, other: Any) -> bool:
        return type(other) == type(self.items) and sorted(other, key=self.key) == sorted(self.items, key=self.key)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.items!r})"


class RegexMatcher:
    """
    pytest helper to check a string against a regex, especially in nested structures, e.g.:

        >>> assert {"foo": "baaaaa"} == {"foo": RegexMatcher("ba+")}
    """

    def __init__(self, pattern: str, flags: int = 0) -> None:
        self.regex = re.compile(pattern=pattern, flags=flags)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, str) and bool(self.regex.match(other))

    def __repr__(self) -> str:
        return self.regex.pattern


class DictSubSet:
    """
    pytest helper to check if a dictionary contains a subset of items, e.g.:

    >> assert {"foo": "bar", "meh": 4} == DictSubSet({"foo": "bar"})
    """

    __slots__ = ["items", "_missing", "_differing"]

    # TODO rename/alias to `a_dict_with()` to be more self-explanatory

    def __init__(self, items: dict[Any | str, Any] | None = None, **kwargs: Any) -> None:
        self.items = {**(items or {}), **kwargs}
        self._missing: dict[Any, Any] | None = None
        self._differing: dict[Any, tuple[Any, Any]] | None = None

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self.items)):
            return False
        self._missing = {k: v for k, v in self.items.items() if k not in other}
        self._differing = {k: (v, other[k]) for k, v in self.items.items() if k in other and other[k] != v}
        return not (self._missing or self._differing)

    def __repr__(self) -> str:
        msg = repr(self.items)
        if self._missing:
            msg += f"\n    # Missing: {self._missing}"
        if self._differing:
            msg += f"\n    # Differing: {self._differing}"
        return msg


class ListSubSet:
    """
    pytest helper to check if a list contains a subset of items, e.g.:

    >> assert [1, 2, 3, 666] == ListSubSet([1, 666])
    """

    # TODO: also take item counts into account?
    def __init__(self, items: list[Any]) -> None:
        self.items = items

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self.items)) and all(any(y == x for y in other) for x in self.items)

    def __repr__(self) -> str:
        return repr(self.items)


########################################## vcr ##########################################
@dataclass
class TestContext:
    __test__ = False

    data_path: Path
    out_path: Path
    caplog: LogCaptureFixture | None

    def __post_init__(self) -> None:
        if self.caplog:
            self.caplog.set_level("DEBUG" if sys.gettrace() is not None else "WARNING")

    def set_log_level(self, level: str | int) -> None:
        if not self.caplog:
            raise RuntimeError("No caplog")
        self.caplog.set_level(level)


def patch_env(key: str, fake_value: str, monkeypatch: MonkeyPatch) -> None:
    """
    Patch an environment variable if it doesn't exist.

    Args:
        key (str): The environment variable key.
        fake_value (str): The fake value to set if the variable doesn't exist.
        monkeypatch (MonkeyPatch): The pytest monkeypatch fixture.
    """
    if not os.environ.get(key):
        monkeypatch.setenv(key, fake_value)


def is_opensearch_uri(uri: str) -> bool:
    """
    Check if a URI is an OpenSearch URI.

    Args:
        uri (str): The URI to check.

    Returns:
        bool: True if the URI is an OpenSearch URI, False otherwise.
    """
    return any(x in uri for x in ["opensearch", "es.amazonaws.com"])


def is_llm_uri(uri: str) -> bool:
    """
    Check if a URI is an LLM URI.

    Args:
        uri (str): The URI to check.

    Returns:
        bool: True if the URI is an LLM URI, False otherwise.
    """
    return any(x in uri for x in ["openai", "llm-proxy", "anthropic", "localhost", "127.0.0.1"])


def is_chroma_uri(uri: str) -> bool:
    """
    Check if a URI is a Chroma URI.

    Args:
        uri (str): The URI to check.

    Returns:
        bool: True if the URI is a Chroma URI, False otherwise.
    """
    return any(x in uri for x in ["localhost", "127.0.0.1"])


def request_matcher(r1: VCRRequest, r2: VCRRequest) -> bool:
    """
    Custom matcher to determine if the requests are the same.

    - For internal adobe requests, we match the parts of the multipart request. This is needed as we can't compare the body
        directly as the chunk boundary is generated randomly
    - For opensearch requests, we just match the body
    - For openai, allow llm-proxy
    - For others, we match both uri and body

    Args:
        r1 (VCRRequest): The first request.
        r2 (VCRRequest): The second request.

    Returns:
        bool: True if the requests match, False otherwise.
    """

    if r1.uri == r2.uri:
        if r1.body == r2.body:
            return True
    elif (
        is_opensearch_uri(r1.uri)
        and is_opensearch_uri(r2.uri)
        or is_llm_uri(r1.uri)
        and is_llm_uri(r2.uri)
        or is_chroma_uri(r1.uri)
        and is_chroma_uri(r2.uri)
    ):
        return r1.body == r2.body

    return False


# SOURCE: https://github.com/kiwicom/pytest-recording/tree/master
def pytest_recording_configure(config: PytestConfig, vcr: VCR) -> None:
    """
    Configure VCR for pytest-recording.

    Args:
        config (PytestConfig): The pytest config object.
        vcr (VCR): The VCR object.
    """
    vcr.register_matcher("request_matcher", request_matcher)
    vcr.match_on = ["request_matcher"]


def filter_response(response: VCRRequest) -> VCRRequest:
    """
    Filter the response before recording.

    If the response has a 'retry-after' header, we set it to 0 to avoid waiting for the retry time.

    Args:
        response (VCRRequest): The response to filter.

    Returns:
        VCRRequest: The filtered response.
    """

    if "retry-after" in response["headers"]:
        response["headers"]["retry-after"] = "0"
    if "x-stainless-arch" in response["headers"]:
        response["headers"]["x-stainless-arch"] = "arm64"

    if "apim-request-id" in response["headers"]:
        response["headers"]["apim-request-id"] = ["9a705e27-2f04-4bd6-abd8-01848165ebbf"]

    if "azureml-model-session" in response["headers"]:
        response["headers"]["azureml-model-session"] = ["d089-20240815073451"]

    if "x-ms-client-request-id" in response["headers"]:
        response["headers"]["x-ms-client-request-id"] = ["9a705e27-2f04-4bd6-abd8-01848165ebbf"]

    if "x-ratelimit-remaining-requests" in response["headers"]:
        response["headers"]["x-ratelimit-remaining-requests"] = ["144"]
    if "x-ratelimit-remaining-tokens" in response["headers"]:
        response["headers"]["x-ratelimit-remaining-tokens"] = ["143324"]
    if "x-request-id" in response["headers"]:
        response["headers"]["x-request-id"] = ["143324"]
    if "Set-Cookie" in response["headers"]:
        response["headers"]["Set-Cookie"] = [
            "__cf_bm=fake;path=/; expires=Tue, 15-Oct-24 23:22:45 GMT; domain=.api.openai.com; HttpOnly;Secure; SameSite=None",
            "_cfuvid=fake;path=/; domain=.api.openai.com; HttpOnly; Secure; SameSite=None",
        ]

    return response


def filter_request(request: VCRRequest) -> VCRRequest | None:
    """
    Filter the request before recording.

    If the request is of type multipart/form-data we don't filter anything, else we perform two additional filterings -
    1. Processes the request body text, replacing today's date with a placeholder.This is necessary to ensure
        consistency in recorded VCR requests. Without this modification, requests would contain varying body text
        with older dates, leading to failures in request body text comparison when executed with new dates.
    2. Filter out specific fields from post data fields

    Args:
        request (VCRRequest): The request to filter.

    Returns:
        Optional[VCRRequest]: The filtered request, or None if the request should be ignored.
    """

    # vcr does not handle multipart/form-data correctly as reported on https://github.com/kevin1024/vcrpy/issues/521
    # so let it pass through as is
    if ctype := request.headers.get("Content-Type"):
        ctype = ctype.decode("utf-8") if isinstance(ctype, bytes) else ctype
        if "multipart/form-data" in ctype:
            return request

    request = copy.deepcopy(request)

    if ".tiktoken" in request.path:
        # request to https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken
        # can be made by ChatLLMInvoker of venice-gentech
        return None

    # filter dates
    if request.body is not None:
        dummy_date_str = "today's date which is DUMMY_DATE"
        request_body_str = request.body.decode("utf-8")
        matches = re.findall(r"today's date which is \d{4}-\d{2}-\d{2}", request_body_str)
        if len(matches) > 0:
            for match in matches:
                request_body_str = request_body_str.replace(match, dummy_date_str)
            request.body = request_body_str.encode("utf-8")

    # filter fields from post
    filter_post_data_parameters = ["api-version", "client_id", "client_secret", "code", "username", "password"]
    replacements = [p if isinstance(p, tuple) else (p, None) for p in filter_post_data_parameters]
    filter_function = functools.partial(filters.replace_post_data_parameters, replacements=replacements)
    request = filter_function(request)

    return request


# SOURCE: https://github.com/kiwicom/pytest-recording/tree/master?tab=readme-ov-file#configuration
# @pytest.fixture(scope="module")
# @pytest.fixture(scope="function")
@pytest.fixture()
def vcr_config() -> dict[str, Any]:
    """
    VCR configuration fixture.

    Returns:
        dict[str, Any]: The VCR configuration.
    """
    return {
        "filter_headers": [
            ("authorization", "DUMMY_AUTHORIZATION"),
            # ("Set-Cookie", "DUMMY_COOKIE"),
            ("x-api-key", "DUMMY_API_KEY"),
            ("api-key", "DUMMY_API_KEY"),
        ],
        "ignore_localhost": False,
        "filter_query_parameters": [
            "api-version",
            "client_id",
            "client_secret",
            "code",
            "api_key",
        ],
        "before_record_request": filter_request,
        "before_record_response": filter_response,
        # !! DO NOT filter post data via a config here, but add it to the filter_data function above !!
        # We don't match requests on 'headers' and 'host' since they vary a lot
        # We tried not matching on 'body' since a POST request - specifically a request to the extract service - appears
        # to have some differences in the body - but that didn't work. Then we didn't get a match at all. So left as is.
        # See https://vcrpy.readthedocs.io/en/latest/configuration.html#request-matching
        # "match_on": ["method", "scheme", "port", "path", "query", "body", "uri"],
        "match_on": ["method", "scheme", "port", "path", "query", "body"],
    }


@pytest.fixture(name="posixpath_fixture")
def posixpath_fixture(monkeypatch: MonkeyPatch) -> None:
    """
    Fixture to monkeypatch os.path to use posixpath.

    This fixture monkeypatches the `os.path` module to use `posixpath` instead of the default `os.path` module.
    It is useful for testing code that relies on POSIX-style paths, regardless of the operating system.

    Args:
    ----
        monkeypatch (MonkeyPatch): The monkeypatch fixture provided by pytest.

    Returns:
    -------
        None

    """
    monkeypatch.setattr(os, "path", posixpath)


@pytest.fixture(name="user_homedir")
def user_homedir() -> str:
    """
    Fixture to get the user's home directory.

    This fixture returns the path to the user's home directory based on the environment.
    It checks if the `GITHUB_ACTOR` environment variable is set, indicating a GitHub Actions environment.
    If `GITHUB_ACTOR` is set, it returns "/Users/runner" as the home directory.
    Otherwise, it returns "/Users/malcolm" as the default home directory.

    Returns:
    -------
        str: The path to the user's home directory.

    """
    return "/Users/runner" if os.environ.get("GITHUB_ACTOR") else "/Users/malcolm"


# # ---------------------------------------------------------------
# # SOURCE: https://github.com/Zorua162/dpystest_minimal/blob/ebbe7f61c741498b8ea8897fc22a11781e4d67bf/conftest.py#L4
# # ---------------------------------------------------------------


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """
    Code to execute after all tests.

    Args:
    ----
        session (pytest.Session): The pytest session object.
        exitstatus (int): The exit status code.

    Returns:
    -------
        None

    """
    # dat files are created when using attachments
    print("\n-------------------------\nClean dpytest_*.dat files")
    fileList = glob.glob("./dpytest_*.dat")
    for filePath in fileList:
        try:
            os.remove(filePath)
        except Exception:
            print("Error while deleting file : ", filePath)


@pytest.fixture()
def mock_ebook_txt_file(tmp_path: Path) -> Path:
    """
    Fixture to create a mock text file for testing purposes.

    This fixture creates a temporary directory and copies a test text file into it.
    The path to the mock text file is then returned for use in tests.

    Args:
    ----
        tmp_path (Path): The temporary path provided by pytest.

    Returns:
    -------
        Path: A Path object of the path to the mock text file.

    """
    test_ebook_txt_path: Path = (
        tmp_path / "The Project Gutenberg eBook of A Christmas Carol in Prose; Being a Ghost Story of Christmas.txt"
    )
    shutil.copy(
        "democracy_exe/data/chroma/documents/The Project Gutenberg eBook of A Christmas Carol in Prose; Being a Ghost Story of Christmas.txt",
        test_ebook_txt_path,
    )
    return test_ebook_txt_path


@pytest.fixture()
def mock_text_documents(mock_ebook_txt_file: FixtureRequest) -> list[Document]:
    loader = TextLoader(f"{mock_ebook_txt_file}")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # Create a unique ID for each document
    # SOURCE: https://github.com/theonemule/azure-rag-sample/blob/1e37de31678ffbbe5361a8ef3acdb770194f462a/import.py#L4
    for idx, doc in enumerate(docs):
        doc.metadata["id"] = str(idx)

    return docs
