import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Optional, TypeVar

import fsspec
from transformers import AutoTokenizer, PreTrainedTokenizerBase
from triad import to_uuid
from triad.utils.convert import get_full_type_path
from fugue_ml.utils.io import unzip_to_temp, zip_temp

T = TypeVar("T")


class HuggingFaceGlobalCachedModel(ABC, Generic[T]):
    def __init__(
        self,
        id_param: str,
        cache_param: str,
        global_cache_dir: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        self.id_param = id_param
        self.cache_param = cache_param
        self.kwargs = dict(kwargs)
        if global_cache_dir is None:
            self.global_cache_file: Optional[str] = None
        else:
            type_id = get_full_type_path(self.__class__)
            self.global_cache_file = os.path.join(
                global_cache_dir,
                "hf-model-" + to_uuid(type_id, kwargs[id_param]) + ".zip",
            )
        self._instance: Any = None

    @abstractmethod  # pragma: no cover
    def construct_instance(self, **kwargs: Any) -> T:
        raise NotImplementedError

    @property
    def instance(self) -> T:
        if self._instance is None:
            self._instance = self.construct_instance(**self.kwargs)
        return self._instance

    def __getstate__(self) -> Dict[str, Any]:
        res = dict(self.__dict__)
        self._serialize()
        del res["_instance"]
        return res

    def __setstate__(self, state: Dict[str, Any]) -> None:
        self.__dict__.update(state)
        self._deserialize()

    def _serialize(self) -> None:
        if self.global_cache_file is not None:
            fs, path = fsspec.core.url_to_fs(self.global_cache_file)
            if not fs.exists(path):
                with zip_temp(self.global_cache_file) as cache_dir:
                    self._instance = self.construct_instance(
                        **self.kwargs, **{self.cache_param: cache_dir}
                    )

    def _deserialize(self) -> None:
        if self.global_cache_file is not None:
            with unzip_to_temp(self.global_cache_file) as cache_dir:
                self._instance = self.construct_instance(
                    **self.kwargs, **{self.cache_param: cache_dir}
                )
        else:
            self._instance = self.construct_instance(**self.kwargs)


class GlobalCachedPretrainedTokenizer(
    HuggingFaceGlobalCachedModel[PreTrainedTokenizerBase]
):
    def __init__(
        self,
        pretrained_model_name_or_path: str,
        global_cache_dir: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(
            id_param="pretrained_model_name_or_path",
            cache_param="cache_dir",
            global_cache_dir=global_cache_dir,
            pretrained_model_name_or_path=pretrained_model_name_or_path,
            **kwargs
        )

    def construct_instance(self, **kwargs: Any) -> PreTrainedTokenizerBase:
        return AutoTokenizer.from_pretrained(**kwargs)
