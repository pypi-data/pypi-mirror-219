##
#   Copyright 2021 Alibaba, Inc. and its affiliates. All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
##

# -*- coding: utf-8 -*-

from enum import Enum, IntEnum
from typing import Union

from dashvector.common.error import DashVectorCode, DashVectorException


class SegmentStrState(str, Enum):
    CREATED = "SS_CREATED"
    MUTABLE = "SS_MUTABLE"
    IMMUTABLE = "SS_IMMUTABLE"
    DUMPING = "SS_DUMPING"
    COMPACTING = "SS_COMPACTING"


class SegmentState(IntEnum):
    CREATED = 0
    MUTABLE = 1
    IMMUTABLE = 2
    DUMPING = 3
    COMPACTING = 4

    @staticmethod
    def get(ss: Union[str, SegmentStrState]):
        if ss == SegmentStrState.CREATED:
            return SegmentState.CREATED
        elif ss == SegmentStrState.MUTABLE:
            return SegmentState.MUTABLE
        elif ss == SegmentStrState.IMMUTABLE:
            return SegmentState.IMMUTABLE
        elif ss == SegmentStrState.DUMPING:
            return SegmentState.DUMPING
        elif ss == SegmentStrState.COMPACTING:
            return SegmentState.COMPACTING
        raise DashVectorException(code=DashVectorCode.InvalidArgument,
                               reason=f'Invalid SegmentState {ss}')


class PartitionStrStatus(str, Enum):
    INITIALIZED = "CS_INITIALIZED"
    SERVING = "CS_SERVING"
    DROPPING = "CS_DROPPING"
    ERROR = "CS_ERROR"


class PartitionStatus(IntEnum):
    INITIALIZED = 0
    SERVING = 1
    DROPPING = 2
    ERROR = 3

    @staticmethod
    def get(ss: Union[str, PartitionStrStatus]) -> IntEnum:
        if ss == PartitionStrStatus.INITIALIZED:
            return PartitionStatus.INITIALIZED
        elif ss == PartitionStrStatus.SERVING:
            return PartitionStatus.SERVING
        elif ss == PartitionStrStatus.DROPPING:
            return PartitionStatus.DROPPING
        elif ss == PartitionStrStatus.ERROR:
            return PartitionStatus.ERROR
        raise DashVectorException(code=DashVectorCode.InvalidArgument,
                               reason=f'Invalid PartitionStatus {ss}')

    @staticmethod
    def str(cs: Union[int, IntEnum]) -> str:
        if cs == PartitionStatus.INITIALIZED:
            return PartitionStrStatus.INITIALIZED.value
        elif cs == PartitionStatus.SERVING:
            return PartitionStrStatus.SERVING.value
        elif cs == PartitionStatus.DROPPING:
            return PartitionStrStatus.DROPPING.value
        elif cs == PartitionStatus.ERROR:
            return PartitionStrStatus.ERROR.value
        raise DashVectorException(code=DashVectorCode.InvalidArgument,
                               reason=f'Invalid PartitionStatus {cs}')


class CollectionStrStatus(str, Enum):
    INITIALIZED = "CS_INITIALIZED"
    SERVING = "CS_SERVING"
    DROPPING = "CS_DROPPING"
    ERROR = "CS_ERROR"


class CollectionStatus(IntEnum):
    INITIALIZED = 0
    SERVING = 1
    DROPPING = 2
    ERROR = 3

    @staticmethod
    def get(cs: Union[str, CollectionStrStatus]) -> IntEnum:
        if cs == CollectionStrStatus.INITIALIZED:
            return CollectionStatus.INITIALIZED
        elif cs == CollectionStrStatus.SERVING:
            return CollectionStatus.SERVING
        elif cs == CollectionStrStatus.DROPPING:
            return CollectionStatus.DROPPING
        elif cs == CollectionStrStatus.ERROR:
            return CollectionStatus.ERROR
        raise DashVectorException(code=DashVectorCode.InvalidArgument,
                               reason=f'Invalid CollectionStatus {cs}')

    @staticmethod
    def str(cs: Union[int, IntEnum]) -> str:
        if cs == CollectionStatus.INITIALIZED:
            return CollectionStrStatus.INITIALIZED.value
        elif cs == CollectionStatus.SERVING:
            return CollectionStrStatus.SERVING.value
        elif cs == CollectionStatus.DROPPING:
            return CollectionStrStatus.DROPPING.value
        elif cs == CollectionStatus.ERROR:
            return CollectionStrStatus.ERROR.value
        raise DashVectorException(code=DashVectorCode.InvalidArgument,
                               reason=f'Invalid CollectionStatus {cs}')