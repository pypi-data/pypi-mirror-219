""" Simple Dataset wrapping an Arrow Table."""

import contextlib
import copy
import itertools
import json
import os
import posixpath
import re
import shutil
import sys
import tempfile
import time
import warnings
import weakref
from collections import Counter
from collections.abc import Mapping
from copy import deepcopy
from fnmatch import fnmatch
from functools import partial, wraps
from io import BytesIO
from math import ceil, floor
from pathlib import Path
from random import sample
from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    Union,
    overload,
)
from typing import Sequence as Sequence_

import fsspec
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
# from huggingface_hub import DatasetCard, DatasetCardData, HfApi, HfFolder
from multiprocessing import Pool
from requests import HTTPError
import logging

logger = logging.get_logger(__name__)

class DatasetInfoMixin:
    """This base class exposes some attributes of DatasetInfo
    at the base level of the Dataset for easy access.
    """

    def __init__(self, info: DatasetInfo, split: Optional[NamedSplit]):
        self._info = info
        self._split = split

    @property
    def info(self):
        """[`~datasets.DatasetInfo`] object containing all the metadata in the dataset."""
        return self._info

    @property
    def split(self):
        """[`~datasets.NamedSplit`] object corresponding to a named dataset split."""
        return self._split

    @property
    def builder_name(self) -> str:
        return self._info.builder_name

    @property
    def citation(self) -> str:
        return self._info.citation

    @property
    def config_name(self) -> str:
        return self._info.config_name

    @property
    def dataset_size(self) -> Optional[int]:
        return self._info.dataset_size

    @property
    def description(self) -> str:
        return self._info.description

    @property
    def download_checksums(self) -> Optional[dict]:
        return self._info.download_checksums

    @property
    def download_size(self) -> Optional[int]:
        return self._info.download_size

    @property
    def features(self) -> Optional[Features]:
        return self._info.features.copy() if self._info.features is not None else None

    @property
    def homepage(self) -> Optional[str]:
        return self._info.homepage

    @property
    def license(self) -> Optional[str]:
        return self._info.license

    @property
    def size_in_bytes(self) -> Optional[int]:
        return self._info.size_in_bytes

    @property
    def supervised_keys(self):
        return self._info.supervised_keys

    @property
    def task_templates(self):
        return self._info.task_templates

    @property
    def version(self):
        return self._info.version

def update_metadata_with_features(table: Table, features: Features):
    """To be used in dataset transforms that modify the features of the dataset, in order to update the features stored in the metadata of its schema."""
    features = Features({col_name: features[col_name] for col_name in table.column_names})
    if table.schema.metadata is None or b"huggingface" not in table.schema.metadata:
        pa_metadata = ArrowWriter._build_metadata(DatasetInfo(features=features))
    else:
        metadata = json.loads(table.schema.metadata[b"huggingface"].decode())
        if "info" not in metadata:
            metadata["info"] = asdict(DatasetInfo(features=features))
        else:
            metadata["info"]["features"] = asdict(DatasetInfo(features=features))["features"]
        pa_metadata = {"huggingface": json.dumps(metadata)}
    table = table.replace_schema_metadata(pa_metadata)
    return table


def _check_table(table) -> Table:
    """We check the table type to make sure it's an instance of :class:`datasets.table.Table`"""
    if isinstance(table, pa.Table):
        # for a pyarrow table, we can just consider it as a in-memory table
        # this is here for backward compatibility
        return InMemoryTable(table)
    elif isinstance(table, Table):
        return table
    else:
        raise TypeError(f"Expected a pyarrow.Table or a datasets.table.Table object, but got {table}.")


def _check_column_names(column_names: List[str]):
    """Check the column names to make sure they don't contain duplicates."""
    counter = Counter(column_names)
    if not all(count == 1 for count in counter.values()):
        duplicated_columns = [col for col in counter if counter[col] > 1]
        raise ValueError(f"The table can't have duplicated columns but columns {duplicated_columns} are duplicated.")

def _check_valid_indices_value(index, size):
    if (index < 0 and index + size < 0) or (index >= size):
        raise IndexError(f"Index {index} out of range for dataset of size {size}.")


class NonExistentDatasetError(Exception):
    """Used when we expect the existence of a dataset"""

    pass

class Dataset(DatasetInfoMixin):
    """

    """