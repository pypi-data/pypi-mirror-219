# Copyright 2021 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict, List, Tuple
from absl.testing import absltest

from temporian.implementation.numpy.data.event_set import EventSet
from temporian.core.data.node import EventSetNode
from temporian.implementation.numpy.data.io import event_set
from temporian.core.operators.prefix import prefix
from temporian.core.operators.glue import glue
from temporian.core.compilation import compile


# TODO: add more extensive tests
# see https://github.com/google/temporian/pull/167#discussion_r1251164852
class CompileTest(absltest.TestCase):
    def setUp(self):
        self.evset = event_set(
            timestamps=[1.0, 2.0, 3.0],
            features={"a": [100.0, 200.0, 300.0]},
        )
        self.other_evset = event_set(
            timestamps=[1.0, 2.0, 3.0],
            features={"b": [100.0, 200.0, 300.0]},
        )

    def test_basic(self):
        @compile
        def f(x: EventSetNode) -> EventSetNode:
            assert isinstance(x, EventSetNode)
            return prefix("a", x)

        result = f(self.evset)

        self.assertEqual(type(result), EventSet)
        self.assertEqual(result.schema.feature_names(), ["aa"])

    def test_composed(self):
        @compile
        def f(x: EventSetNode) -> EventSetNode:
            assert isinstance(x, EventSetNode)
            return glue(
                prefix("a", x),
                prefix("b", x),
            )

        result = f(self.evset)

        self.assertEqual(type(result), EventSet)
        self.assertEqual(result.schema.feature_names(), ["aa", "ba"])

    def test_other_args(self):
        @compile
        def f(a: int, x: EventSetNode, b: str) -> EventSetNode:
            assert isinstance(x, EventSetNode)
            return prefix(f"{a}_{b}_", x)

        result = f(1, self.evset, "a")

        self.assertEqual(type(result), EventSet)
        self.assertEqual(result.schema.feature_names(), ["1_a_a"])

    def test_tuple_arg(self):
        @compile
        def f(x: Tuple[EventSetNode]) -> EventSetNode:
            assert isinstance(x, tuple)
            assert all(isinstance(n, EventSetNode) for n in x)
            return prefix("a", x[0])

        result = f((self.evset, self.other_evset))

        self.assertEqual(type(result), EventSet)
        self.assertEqual(result.schema.feature_names(), ["aa"])

    def test_list_arg(self):
        @compile
        def f(x: List[EventSetNode]) -> EventSetNode:
            assert isinstance(x, list)
            assert all(isinstance(n, EventSetNode) for n in x)
            return prefix("a", x[0])

        result = f([self.evset, self.other_evset])

        self.assertEqual(type(result), EventSet)
        self.assertEqual(result.schema.feature_names(), ["aa"])

    def test_dict_arg(self):
        @compile
        def f(x: Dict[str, EventSetNode]) -> EventSetNode:
            assert isinstance(x, dict)
            assert all(isinstance(n, EventSetNode) for n in x.values())
            return prefix("a", list(x.values())[0])

        result = f({"a": self.evset, "b": self.other_evset})

        self.assertEqual(type(result), EventSet)
        self.assertEqual(result.schema.feature_names(), ["aa"])

    def test_list_return(self):
        @compile
        def f(x: EventSetNode) -> List[EventSetNode]:
            return [prefix("a", x), prefix("b", x)]

        result = f(self.evset)

        self.assertTrue(isinstance(result, list))
        self.assertEqual(len(result), 2)
        self.assertEqual(type(result[0]), EventSet)
        self.assertEqual(type(result[1]), EventSet)
        self.assertEqual(result[0].schema.feature_names(), ["aa"])
        self.assertEqual(result[1].schema.feature_names(), ["ba"])

    def test_dict_return(self):
        @compile
        def f(x: EventSetNode) -> Dict[str, EventSetNode]:
            return {"a": prefix("a", x), "b": prefix("b", x)}

        result = f(self.evset)

        self.assertTrue(isinstance(result, dict))
        self.assertEqual(len(result), 2)
        self.assertEqual(type(result["a"]), EventSet)
        self.assertEqual(type(result["b"]), EventSet)
        self.assertEqual(result["a"].schema.feature_names(), ["aa"])
        self.assertEqual(result["b"].schema.feature_names(), ["ba"])

    def test_mixed_args(self):
        @compile
        def f(x: EventSetNode, y: EventSetNode) -> EventSetNode:
            return glue(x, y)

        with self.assertRaisesRegex(
            ValueError, "Cannot mix EventSets and EventSetNodes"
        ):
            f({"a": self.evset, "b": self.other_evset.node()})

        with self.assertRaisesRegex(
            ValueError, "Cannot mix EventSets and EventSetNodes"
        ):
            f({"a": self.evset.node(), "b": self.other_evset})


if __name__ == "__main__":
    absltest.main()
