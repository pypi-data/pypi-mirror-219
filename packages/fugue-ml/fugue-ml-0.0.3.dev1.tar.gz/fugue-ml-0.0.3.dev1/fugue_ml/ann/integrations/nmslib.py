from typing import Any, Dict, Optional

import nmslib
import numpy as np
import pandas as pd

from fugue_ml.ann.indexer import ANNLocalIndexer
from fugue_ml.utils.io import SharedFile
import os


class NMSLibIndexer(ANNLocalIndexer):
    def build_local(self, arr: np.ndarray, **kwargs) -> ANNLocalIndexer:
        index = self._init_index()
        index.addDataPointBatch(arr)
        index.createIndex(kwargs)
        index.setQueryTimeParams(self.search_params)
        return self

    def search_index_local(
        self,
        df: pd.DataFrame,
        top_n: int,
        idx_col: str,
        dist_col: Optional[str],
        remove_vec_col: bool,
        **kwargs: Any,
    ) -> pd.DataFrame:
        narr = self.get_np_arr(df)
        res = self.index.knnQueryBatch(narr, k=top_n, **kwargs)  # type: ignore
        cols = {idx_col: [x[0] for x in res]}
        if dist_col is not None:
            cols[dist_col] = [x[1] for x in res]
        if remove_vec_col:
            df = df.drop(columns=[self.vec_col])
        df = df.assign(**cols)
        del narr, res, cols
        return df

    def __getstate__(self) -> Dict[str, Any]:
        if not hasattr(self, "_index_file"):
            sf = SharedFile()
            with sf.zip_temp() as tmpdir:
                self.index.saveIndex(os.path.join(tmpdir, "index.bin"), save_data=True)
                if self.local_index_df is not None:
                    self.local_index_df.to_parquet(
                        os.path.join(tmpdir, "index.parquet")
                    )
            self._index_file = sf
        state = self.__dict__.copy()
        del state["index"], state["local_index_df"]
        return state

    def __setstate__(self, state: Dict[str, Any]) -> None:
        for k, v in state.items():
            setattr(self, k, v)
        index = self._init_index()
        with state["_index_file"].unzip_to_temp() as tmpdir:
            index.loadIndex(os.path.join(tmpdir, "index.bin"), load_data=True)
            index.setQueryTimeParams(self.search_params)
            self.local_index_df = pd.read_parquet(os.path.join(tmpdir, "index.parquet"))

    def _init_index(self) -> Any:
        if self.metric == "cos":
            space = "cosinesimil"
        elif self.metric == "l2":
            space = "l2"
        else:
            raise ValueError(f"metric {self.metric} is not supported")
        index = nmslib.init(space=space, **self.init_params)
        self.index = index
        return index
