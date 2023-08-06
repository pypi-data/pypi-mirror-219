import os
from io import BytesIO

from fugue import register_global_conf
import fsspec

from fugue_ml.utils.io import SharedFile, unzip_to_temp, zip_temp


def test_zip_unzip(tmpdir):
    bio = BytesIO()
    with zip_temp(bio) as tmp:
        fs, path = fsspec.core.url_to_fs(tmp)
        fs.write_text(os.path.join(path, "a.txt"), "a")
        fs.write_text(os.path.join(path, "b.txt"), "b")

    with unzip_to_temp(BytesIO(bio.getvalue())) as tmp:
        fs, path = fsspec.core.url_to_fs(tmp)
        assert fs.read_text(os.path.join(path, "a.txt")) == "a"
        assert fs.read_text(os.path.join(path, "b.txt")) == "b"

    tf = os.path.join(str(tmpdir), "temp", "x.zip")
    with zip_temp(tf) as tmp:
        fs, path = fsspec.core.url_to_fs(tmp)
        fs.write_text(os.path.join(path, "a.txt"), "a")
        fs.write_text(os.path.join(path, "b.txt"), "b")

    with unzip_to_temp(tf) as tmp:
        fs, path = fsspec.core.url_to_fs(tmp)
        assert fs.read_text(os.path.join(path, "a.txt")) == "a"
        assert fs.read_text(os.path.join(path, "b.txt")) == "b"


def test_shared_file(tmpdir):
    sf = SharedFile(str(tmpdir))
    with sf.zip_temp() as tmp:
        fs, path = fsspec.core.url_to_fs(tmp)
        fs.write_text(os.path.join(path, "a.txt"), "a")
        fs.write_text(os.path.join(path, "b.txt"), "b")

    with sf.unzip_to_temp() as tmp:
        fs, path = fsspec.core.url_to_fs(tmp)
        assert fs.read_text(os.path.join(path, "a.txt")) == "a"
        assert fs.read_text(os.path.join(path, "b.txt")) == "b"

    register_global_conf({"fugue.ml.cache.path": os.path.join(str(tmpdir) + "/x")})
    sf = SharedFile()
    assert sf.folder == os.path.join(str(tmpdir) + "/x")
