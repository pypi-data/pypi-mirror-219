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

from dashvector.version import __version__
from dashvector.common.error import DashVectorCode, DashVectorException
from dashvector.common.status import CollectionStatus, PartitionStatus
from dashvector.common.types import DashVectorProtocol, DashVectorResponse
from dashvector.common.types import DataType, CollectionMeta, CollectionStats, CollectionField
from dashvector.core.partition import PartitionMeta, PartitionStats
from dashvector.core.doc import Doc
from dashvector.core.collection import Collection
from dashvector.core.client import Client
