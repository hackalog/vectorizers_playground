"""
Custom dataset processing/generation functions should be added to this file
"""

import pathlib
from sklearn.datasets import fetch_20newsgroups
from functools import partial

from .. import workflow, paths
from ..log import logger

from tqdm.auto import tqdm

__all__ = [
'process_20_newsgroups'
]


def process_20_newsgroups(*, extract_dir='20_newsgroups',
                          metadata=None, unpack_dir=None,
                          opts={"subset":"all", "remove":"('headers', 'footers', 'quotes')"}):
    """
    Process 20 newsgroups into (data, target, metadata) format.


    Parameters
    ----------
    unpack_dir: path
        The interim parent directory the dataset files have been unpacked into.
    extract_dir: str
        Name of the directory of the unpacked files relative to the unpack_dir. Note that
    opts: dict default {"subset":"all", "remove"="('headers', 'footers', 'quotes')"}
        Options to pass to sklearn.datasets.fetch_20newsgroups.


    Returns
    -------
    A tuple:
        (data, target, additional_metadata)

    """
    if metadata is None:
        metadata = {}

    if unpack_dir is None:
        unpack_dir = paths['interim_data_path']
    else:
        unpack_dir = pathlib.Path(unpack_dir)
    data_dir = unpack_dir / f"{extract_dir}"

    news = fetch_20newsgroups(**opts)
    metadata['target_names'] = news.target_names

    return news.data, news.target, metadata
