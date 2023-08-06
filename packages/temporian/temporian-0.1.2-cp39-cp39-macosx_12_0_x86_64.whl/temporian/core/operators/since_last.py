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

"""Resample operator class and public API function definition."""

from typing import Optional

from temporian.core import operator_lib
from temporian.core.compilation import compile
from temporian.core.data.node import (
    EventSetNode,
    create_node_new_features_existing_sampling,
)
from temporian.core.operators.base import Operator
from temporian.proto import core_pb2 as pb
from temporian.core.data.dtype import DType


class SinceLast(Operator):
    def __init__(
        self,
        input: EventSetNode,
        sampling: Optional[EventSetNode] = None,
    ):
        super().__init__()

        self.add_input("input", input)

        if sampling is not None:
            self.add_input("sampling", sampling)
            self._has_sampling = True
            effective_sampling_node = sampling
            input.schema.check_compatible_index(sampling.schema)

        else:
            effective_sampling_node = input
            self._has_sampling = False

        self.add_output(
            "output",
            create_node_new_features_existing_sampling(
                features=[("since_last", DType.FLOAT64)],
                sampling_node=effective_sampling_node,
                creator=self,
            ),
        )
        self.check()

    @classmethod
    def build_op_definition(cls) -> pb.OperatorDef:
        return pb.OperatorDef(
            key="SINCE_LAST",
            attributes=[],
            inputs=[
                pb.OperatorDef.Input(key="input"),
                pb.OperatorDef.Input(key="sampling", is_optional=True),
            ],
            outputs=[pb.OperatorDef.Output(key="output")],
        )

    @property
    def has_sampling(self) -> bool:
        return self._has_sampling


operator_lib.register_operator(SinceLast)


@compile
def since_last(
    input: EventSetNode,
    sampling: Optional[EventSetNode] = None,
) -> EventSetNode:
    """Computes the amount of time since the last distinct timestamp.

    Example 1:
        ```python
        >>> a = tp.event_set(timestamps=[1, 5, 8, 8, 9])
        >>> b = tp.since_last(a)
        >>> b
        indexes: ...
                timestamps: [1. 5. 8. 8. 9.]
                'since_last': [nan  4.  3.  0.  1.]
        ...

        ```

    Example 2:
        ```python
        >>> a = tp.event_set(timestamps=[2, 5, 7])
        >>> b = tp.event_set(timestamps=[1, 4, 6, 10])

        >>> # Time elapsed between each sampling event
        >>> # and the latest previous event in a
        >>> c = tp.since_last(a, sampling=b)
        >>> c
        indexes: ...
                timestamps: [ 1. 4. 6. 10.]
                'since_last': [nan  2.  1.  3.]
        ...

        ```

    Args:
        input: Event to sample.
        sampling: Event to use the sampling of.

    Returns:
        Resampled event, with same sampling as `sampling`.
    """

    return SinceLast(input=input, sampling=sampling).outputs["output"]
