from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Tuple, cast

from qiniu import Auth, BucketManager, build_batch_delete, etag, put_file
from qiniu.http import ResponseInfo

from beni import bfunc, bhttp, bpath, bzip


class QiniuItem:
    def __init__(self, data: Any) -> None:
        self.key = data['key']
        self.size = data['fsize']
        self.qetag = data['hash']
        self.time = data['putTime']


_ListResult = tuple[
    dict[str, Any],
    Any,
    Any,
]


class QiniuBucket():

    def __init__(self, bucket: str, url: str, ak: str, sk: str) -> None:
        self.q = Auth(ak, sk)
        self.bucket = bucket
        self.url = url

    async def upload(self, key: str, file: Path | str):
        token = self.q.upload_token(self.bucket, key)
        _, info = await bfunc.run_thread(
            lambda: cast(Tuple[Any, ResponseInfo], put_file(token, key, file, version='v2'))
        )
        assert info.exception is None
        assert info.status_code == 200

    def get_url(self, key: str):
        return self.q.private_download_url(f'{self.url}/{key}')

    @asynccontextmanager
    async def _download(self, key: str):
        url = self.get_url(key)
        async with bpath.use_temp_file() as tempfile:
            await bhttp.download(url, tempfile)
            assert tempfile.exists()
            yield tempfile

    async def download(self, key: str, file: Path | str, force: bool = False):
        async with self._download(key) as tempfile:
            await bpath.move(tempfile, file, force)

    async def download_unzip(self, key: str, output: Path | str):
        async with self._download(key) as tempfile:
            async with bpath.use_temp_dir() as tempdir:
                await bzip.unzip(tempfile, tempdir)
                await bpath.move_children(tempdir, output, True)

    async def download_seven_unzip(self, key: str, output: Path | str):
        async with self._download(key) as tempfile:
            async with bpath.use_temp_dir() as tempdir:
                await bzip.seven_unzip(tempfile, tempdir)
                await bpath.move_children(tempdir, output, True)

    async def get_list(self, prefix: str, limit: int = 100):
        bucket = BucketManager(self.q)
        result, _, _ = await bfunc.run_thread(
            lambda: cast(_ListResult, bucket.list(self.bucket, prefix, None, limit))
        )
        assert type(result) is dict
        ary = [QiniuItem(x) for x in result['items']]
        return ary, cast(str | None, result.get('marker', None))

    async def get_list_by_marker(self, marker: str, limit: int = 100):
        bucket = BucketManager(self.q)
        result, _, _ = await bfunc.run_thread(
            lambda: cast(_ListResult, bucket.list(self.bucket, None, marker, limit))
        )
        assert type(result) is dict
        ary = [QiniuItem(x) for x in result['items']]
        return ary, cast(str | None, result.get('marker', None))

    async def delete_files(self, *keyList: str):
        bucket = BucketManager(self.q)
        result, _ = await bfunc.run_thread(
            lambda: cast(tuple[Any, Any], bucket.batch(build_batch_delete(self.bucket, keyList)))
        )
        assert result

    async def hash_file(self, file: Path | str):
        return await bfunc.run_thread(
            lambda: etag(file)
        )
