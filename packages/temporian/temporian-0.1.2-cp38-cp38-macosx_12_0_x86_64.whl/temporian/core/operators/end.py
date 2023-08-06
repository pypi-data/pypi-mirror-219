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


"""End operator class and public API function definitions."""

from temporian.core import operator_lib
from temporian.core.compilation import compile
from temporian.core.data.node import (
    EventSetNode,
    create_node_new_features_new_sampling,
)
from temporian.core.operators.base import Operator
from temporian.proto import core_pb2 as pb


class EndOperator(Operator):
    def __init__(self, input: EventSetNode):
        super().__init__()

        self.add_input("input", input)

        self.add_output(
            "output",
            create_node_new_features_new_sampling(
                features=[],
                indexes=input.schema.indexes,
                is_unix_timestamp=input.schema.is_unix_timestamp,
                creator=self,
            ),
        )
        self.check()

    @classmethod
    def build_op_definition(cls) -> pb.OperatorDef:
        return pb.OperatorDef(
            key="END",
            attributes=[],
            inputs=[pb.OperatorDef.Input(key="input")],
            outputs=[pb.OperatorDef.Output(key="output")],
        )


operator_lib.register_operator(EndOperator)


@compile
def end(input: EventSetNode) -> EventSetNode:
    """Generates a single timestamp at the end of the input, per index.

    Usage example:
        ```python
        >>> a = tp.event_set(
        ...     timestamps=[5, 6, 7, 1],
        ...     features={"f": [50, 60, 70, 10], "idx": [1, 1, 1, 2]},
        ...     indexes=["idx"]
        ... )

        >>> a_end = tp.end(a)
        >>> a_end
        indexes: [('idx', int64)]
        features: []
        events:
            idx=2 (1 events):
                timestamps: [1.]
            idx=1 (1 events):
                timestamps: [7.]
        ...

        ```

    Args:
        input: Guide input

    Returns:
        A feature-less node with a single timestamp.
    """

    return EndOperator(input=input).outputs["output"]
