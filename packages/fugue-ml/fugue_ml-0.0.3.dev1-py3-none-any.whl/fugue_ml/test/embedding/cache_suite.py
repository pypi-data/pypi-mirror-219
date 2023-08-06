from unittest import TestCase

import fugue.api as fa
import pandas as pd

from fugue_ml.embedding.cache import EmbeddingCache


class EmbeddingCacheTests(object):
    class Tests(TestCase):
        @classmethod
        def setUpClass(cls):
            pass

        @classmethod
        def tearDownClass(cls):
            pass

        def create_cache(self) -> EmbeddingCache:
            raise NotImplementedError

        def test_cache(self):
            with self.create_cache() as cache:
                query = pd.DataFrame(dict(a=[1, 4], b=["a", "d"]))  # noqa
                cached, new_df = cache.query(query, uid_col="a", vec_col="c")
                assert cached is None or fa.count(cached) == 0
                assert fa.count(new_df) == 2
                assert fa.get_schema(new_df) == fa.get_schema(query)

                assert cache.find_new(query, uid_col="a").sort_values(
                    ["a"]
                ).values.tolist() == [[1, "a"], [4, "d"]]

                data = pd.DataFrame(
                    dict(  # noqa
                        a=[1, 2, 3],
                        b=[[0, 1], [2, 3], [4, 5]],
                    )
                )
                cache.upsert(data, uid_col="a", vec_col="b")

                cached, new_df = cache.query(query, uid_col="a", vec_col="c")
                assert fa.as_array(cached, type_safe=True) == [[1, "a", [0, 1]]]
                assert fa.count(new_df) == 1
                assert fa.get_schema(new_df) == fa.get_schema(query)
                assert fa.as_array(new_df) == [[4, "d"]]

                assert cache.find_new(query, uid_col="a").sort_values(
                    ["a"]
                ).values.tolist() == [[4, "d"]]

                data = pd.DataFrame(
                    dict(  # noqa
                        aa=[1, 4, 5],
                        bb=[[10, 20], [20, 30], [40, 50]],
                    )
                )
                cache.upsert(data, uid_col="aa", vec_col="bb")
                cached, new_df = cache.query(query, uid_col="a", vec_col="c")
                assert fa.as_array(
                    fa.as_pandas(cached).sort_values(["a"]).reset_index(drop=True),
                    type_safe=True,
                ) == [
                    [1, "a", [10, 20]],
                    [4, "d", [20, 30]],
                ]
                assert new_df is None or fa.count(new_df) == 0

                new_df = cache.find_new(query, uid_col="a")
                assert new_df is None or fa.count(new_df) == 0
