import os
import tempfile
import zipfile
from contextlib import contextmanager
from typing import Any, Iterator, Optional
from uuid import uuid4

import fsspec
import fugue.api as fa

from fugue_ml.constants import FUGUE_ML_CONF_CACHE_PATH


def get_temp_dir() -> str:
    return fa.get_current_conf().get_or_throw(FUGUE_ML_CONF_CACHE_PATH, str)


@contextmanager
def zip_temp(fobj: Any) -> Iterator[str]:
    """Zip a temporary directory to a file object.

    :param fobj: the file path or file object

    .. admonition:: Examples

        .. code-block:: python

            from fugue_ml.utils.io import zip_temp
            from io import BytesIO

            bio = BytesIO()
            with zip_temp(bio) as tmpdir:
                # do something with tmpdir (string)
    """
    if isinstance(fobj, str):
        with fsspec.open(fobj, "wb") as f:
            with zip_temp(f) as tmpdir:
                yield tmpdir
    else:
        with tempfile.TemporaryDirectory() as tmpdirname:
            yield tmpdirname

            with zipfile.ZipFile(
                fobj, "w", zipfile.ZIP_DEFLATED, allowZip64=True
            ) as zf:
                for root, _, filenames in os.walk(tmpdirname):
                    for name in filenames:
                        file_path = os.path.join(root, name)
                        rel_dir = os.path.relpath(root, tmpdirname)
                        rel_name = os.path.normpath(os.path.join(rel_dir, name))
                        zf.write(file_path, rel_name)


@contextmanager
def unzip_to_temp(fobj: Any) -> Iterator[str]:
    """Unzip a file object into a temporary directory.

    :param fobj: the file object

    .. admonition:: Examples

        .. code-block:: python

            from fugue_ml.utils.io import zip_temp
            from io import BytesIO

            bio = BytesIO()
            with zip_temp(bio) as tmpdir:
                # create files in the tmpdir (string)

            with unzip_to_temp(BytesIO(bio.getvalue())) as tmpdir:
                # read files from the tmpdir (string)
    """
    if isinstance(fobj, str):
        with fsspec.open(fobj, "rb") as f:
            with unzip_to_temp(f) as tmpdir:
                yield tmpdir
    else:
        with tempfile.TemporaryDirectory() as tmpdirname:
            with zipfile.ZipFile(fobj, "r") as zip_ref:
                zip_ref.extractall(tmpdirname)

            yield tmpdirname


class SharedFile:
    """A file that can be shared across machines.

    :param folder: the folder to store the temp file, if not specified,
        it will use the config value of ``fugue.ml.cache.path``
    """

    def __init__(self, folder: Optional[str] = None):
        self.folder = folder or get_temp_dir()
        self.path = os.path.join(self.folder, str(uuid4()) + ".bin")

    @contextmanager
    def zip_temp(self) -> Iterator[str]:
        """Zip a temporary directory to the shared file.

        .. admonition:: Examples

            .. code-block:: python

                from fugue_ml.utils.io import SharedFile

                sf = SharedFile()
                with sf.zip_temp() as tmpdir:
                    # do something with tmpdir (string)
        """
        with zip_temp(self.path) as tmpdir:
            yield tmpdir

    @contextmanager
    def unzip_to_temp(self) -> Iterator[str]:
        """Unzip a file object into a temporary directory.

        .. admonition:: Examples

            .. code-block:: python

                from fugue_ml.utils.io import SharedFile

                sf = SharedFile()
                with sf.zip_temp() as tmpdir:
                    # create files in the tmpdir (string)

                with sf.unzip_to_temp() as tmpdir:
                    # read files from the tmpdir (string)
        """
        with unzip_to_temp(self.path) as tmpdir:
            yield tmpdir
