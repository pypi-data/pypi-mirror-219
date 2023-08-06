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

import struct

from enum import Enum, IntEnum
from typing import Type, Dict, Any, List, Tuple, Union, Optional

import json
import numpy as np

from dashvector.common.constants import DASHVECTOR_VECTOR_NAME
from dashvector.common.error import DashVectorCode, DashVectorException
from dashvector.common.status import CollectionStatus
from dashvector.common.handler import RPCResponse
from dashvector.core.partition import PartitionMetaBuilder, PartitionStatsBuilder

VectorDataType = Union[Type[int], Type[float], Type[bool], Type[np.int8], Type[np.int16], Type[np.float16], Type[np.bool_], Type[np.float32], Type[np.float64]]
VectorValueType = Union[List[Union[int, float]], np.ndarray]
FieldDataType = Dict[str, Union[Type[str], Type[int], Type[float], Type[bool]]]
FieldValueType = Dict[str, Union[str, int, float, bool]]
IdType = Union[str, int]
IdsType = Union[IdType, List[IdType]]
ValueDataType = Union[str, int, float, bool]


class DashVectorProtocol(IntEnum):
    GRPC = 0
    HTTP = 1


class IndexStrType(str, Enum):
    UNDEFINED = "IT_UNDEFINED"
    HNSW = "IT_HNSW"
    INVERT = "IT_INVERT"


class IndexType(IntEnum):
    UNDEFINED = 0
    HNSW = 1
    INVERT = 10

    @staticmethod
    def get(itype: Union[str, IndexStrType]):
        if itype == IndexStrType.UNDEFINED:
            return IndexType.UNDEFINED
        elif itype == IndexStrType.HNSW:
            return IndexType.HNSW
        elif itype == IndexStrType.INVERT:
            return IndexType.INVERT
        else:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f'Invalid IndexType {itype}')

    @staticmethod
    def str(itype: Union[int, IntEnum]) -> str:
        if itype == IndexType.UNDEFINED:
            return IndexStrType.UNDEFINED.value
        elif itype == IndexType.HNSW:
            return IndexStrType.HNSW.value
        elif itype == IndexType.INVERT:
            return IndexStrType.INVERT.value
        raise DashVectorException(code=DashVectorCode.InvalidArgument,
                               reason=f'Invalid IndexType {cs}')


class DataStrType(str, Enum):
    UNDEFINED = "DT_UNDEFINED"
    BINARY = "DT_BINARY"
    STRING = "DT_STRING"
    BOOL = "DT_BOOL"
    INT32 = "DT_INT32"
    INT64 = "DT_INT64"
    UINT32 = "DT_UINT32"
    UINT64 = "DT_UINT64"
    FLOAT = "DT_FLOAT"
    DOUBLE = "DT_DOUBLE"
    VECTOR_FP16 = "DT_VECTOR_FP16"
    VECTOR_FP32 = "DT_VECTOR_FP32"
    VECTOR_FP64 = "DT_VECTOR_FP64"
    VECTOR_INT4 = "DT_VECTOR_INT4"
    VECTOR_INT8 = "DT_VECTOR_INT8"
    VECTOR_INT16 = "DT_VECTOR_INT16"
    VECTOR_BINARY32 = "DT_VECTOR_BINARY32"
    VECTOR_BINARY64 = "DT_VECTOR_BINARY64"

    def __str__(self):
        return self.value


class DataType(IntEnum):
    UNDEFINED = 0
    BINARY = 1
    STRING = 2
    BOOL = 3
    INT32 = 4
    INT64 = 5
    UINT32 = 6
    UINT64 = 7
    FLOAT = 8
    DOUBLE = 9
    VECTOR_BINARY32 = 20
    VECTOR_BINARY64 = 21
    VECTOR_FP16 = 22
    VECTOR_FP32 = 23
    VECTOR_FP64 = 24
    VECTOR_INT4 = 25
    VECTOR_INT8 = 26
    VECTOR_INT16 = 27

    @staticmethod
    def get(dtype: Union[str, DataStrType]) -> IntEnum:
        if dtype == DataStrType.UNDEFINED:
            return DataType.UNDEFINED
        elif dtype == DataStrType.BINARY:
            return DataType.BINARY
        elif dtype == DataStrType.STRING:
            return DataType.STRING
        elif dtype == DataStrType.BOOL:
            return DataType.BOOL
        elif dtype == DataStrType.INT32:
            return DataType.INT32
        elif dtype == DataStrType.INT64:
            return DataType.INT64
        elif dtype == DataStrType.UINT32:
            return DataType.UINT32
        elif dtype == DataStrType.UINT64:
            return DataType.UINT64
        elif dtype == DataStrType.FLOAT:
            return DataType.FLOAT
        elif dtype == DataStrType.DOUBLE:
            return DataType.DOUBLE
        elif dtype == DataStrType.VECTOR_FP16:
            return DataType.VECTOR_FP16
        elif dtype == DataStrType.VECTOR_FP32:
            return DataType.VECTOR_FP32
        elif dtype == DataStrType.VECTOR_FP64:
            return DataType.VECTOR_FP64
        elif dtype == DataStrType.VECTOR_INT4:
            return DataType.VECTOR_INT4
        elif dtype == DataStrType.VECTOR_INT8:
            return DataType.VECTOR_INT8
        elif dtype == DataStrType.VECTOR_INT16:
            return DataType.VECTOR_INT16
        elif dtype == DataStrType.VECTOR_BINARY32:
            return DataType.VECTOR_BINARY32
        elif dtype == DataStrType.VECTOR_BINARY64:
            return DataType.VECTOR_BINARY64
        else:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f'Invalid DataType {dtype}')

    @staticmethod
    def str(dtype: Union[int, IntEnum]) -> str:
        if dtype == DataType.UNDEFINED:
            return "undefiled"
        elif dtype == DataType.BINARY:
            return "bytes"
        elif dtype == DataType.STRING:
            return "str"
        elif dtype == DataType.BOOL:
            return "bool"
        elif dtype == DataType.INT32:
            return "int"
        elif dtype == DataType.INT64:
            return "int"
        elif dtype == DataType.UINT32:
            return "int"
        elif dtype == DataType.UINT64:
            return "int"
        elif dtype == DataType.FLOAT:
            return "float"
        elif dtype == DataType.DOUBLE:
            return "float"
        elif dtype == DataType.VECTOR_FP16:
            return "float"
        elif dtype == DataType.VECTOR_FP32:
            return "float"
        elif dtype == DataType.VECTOR_FP64:
            return "float"
        elif dtype == DataType.VECTOR_INT4:
            return "int"
        elif dtype == DataType.VECTOR_INT8:
            return "int"
        elif dtype == DataType.VECTOR_INT16:
            return "int"
        elif dtype == DataType.VECTOR_BINARY32:
            return "bytes"
        elif dtype == DataType.VECTOR_BINARY64:
            return "bytes"
        else:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f'Invalid DataType {dtype}')


_vector_dtype_map = {
    float: DataType.VECTOR_FP32,
    int: DataType.VECTOR_INT8,
    np.float32: DataType.VECTOR_FP32
}

_attr_dtype_map = {
    str: DataType.STRING,
    bool: DataType.BOOL,
    int: DataType.INT32,
    float: DataType.FLOAT
}


class CollectionField(object):
    def __init__(self,
                 *,
                 field_name: str,
                 index_type: IndexStrType = IndexStrType.UNDEFINED,
                 data_type: DataStrType = DataStrType.UNDEFINED,
                 dimension: int):
        self._field_name = field_name
        self._index_type = IndexType.get(index_type)
        self._data_type = DataType.get(data_type)
        self._dimension = dimension

    @property
    def field_name(self):
        return self._field_name

    @property
    def index_type(self):
        return self._index_type

    @property
    def data_type(self):
        return self._data_type

    @property
    def dimension(self):
        return self._dimension

    def __dict__(self):
        meta_dict = {
            'field_name': self.field_name
        }
        if self.data_type != DataType.UNDEFINED:
            meta_dict['data_type'] = DataType.str(self.data_type)
        if self.index_type != IndexType.UNDEFINED:
            meta_dict['index_type'] = IndexType.str(self.index_type)
        if self.dimension > 0:
            meta_dict['dimension'] = self.dimension
        return meta_dict

    def __str__(self):
        return json.dumps(self.__dict__())

    def __repr__(self):
        return self.__str__()


class CollectionMeta(object):
    def __init__(self,
                 *,
                 meta: Dict):

        """
        meta: Dict
        """
        self._meta = meta
        if not isinstance(meta, dict):
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason="DashVectorSDK Collection Meta is Invalid")

        """
        schema: Dict
        """
        self._schema = None
        if 'schema' in self._meta and isinstance(self._meta['schema'], dict):
            self._schema = self._meta['schema']
        else:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason="DashVectorSDK Collection Schema is Invalid")

        """
        name: str
        """
        self._name = ""
        if 'collection_name' in self._schema and isinstance(self._schema['collection_name'], str):
            self._name = self._schema['collection_name']
        else:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason="DashVectorSDK Collection Schema is Invalid")

        """
        dimension: 1024,
        dtype: float,
        metric: "euclidean",
        fields: List[CollectionField]
        """
        self._dimension = 0
        self._dtype = DataType.VECTOR_FP32
        self._metric = "euclidean"
        self._vector_field = None
        self._fields = []
        self._fields_len = 0
        if 'fields' in self._schema and isinstance(self._schema['fields'], list):
            for field in self._schema['fields']:

                field_name = ""
                if 'field_name' in field and isinstance(field['field_name'], str):
                    field_name = field['field_name']
                else:
                    raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                           reason="DashVectorSDK Collection Schema is Invalid")

                if field_name == DASHVECTOR_VECTOR_NAME:
                    if 'dimension' not in field:
                        raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                               reason="DashVectorSDK Collection Schema is Invalid")
                    self._dimension = int(field['dimension'])

                    if 'data_type' not in field:
                        raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                               reason="DashVectorSDK Collection Schema is Invalid")
                    self._dtype = DataType.get(field['data_type'])

                    if 'extra_params' in field and isinstance(field['extra_params'], list):
                        for extra_param in field['extra_params']:
                            if 'key' in extra_param and 'value' in extra_param \
                                    and extra_param['key'] == "metric_type"\
                                    and isinstance(extra_param['value'], str):
                                if extra_param['value'] == "SquaredEuclidean":
                                    self._metric = "euclidean"
                                elif extra_param['value'] == "InnerProduct":
                                    self._metric = "dotproduct"
                                elif extra_param['value'] == "Cosine":
                                    self._metric = "cosine"
                                else:
                                    self._metric = extra_param['value']
                                break

                    self._vector_field = CollectionField(field_name=field['field_name'],
                                                         index_type=field['index_type'] if 'index_type' in field else IndexStrType.UNDEFINED,
                                                         data_type=field['data_type'] if 'data_type' in field else DataStrType.UNDEFINED,
                                                         dimension=field['dimension'] if 'dimension' in field else 0)
                else:
                    self._fields_len += 1
                    self._fields.append(CollectionField(field_name=field['field_name'],
                                                        index_type=field['index_type'] if 'index_type' in field else IndexStrType.UNDEFINED,
                                                        data_type=field['data_type'] if 'data_type' in field else DataStrType.UNDEFINED,
                                                        dimension=field['dimension'] if 'dimension' in field else 0))
        else:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason="DashVectorSDK Collection Schema is Invalid")

        """
        state: str
        """
        self._state = None
        if 'collection_status' in self._meta and isinstance(self._meta['collection_status'], str):
            self._state = CollectionStatus.get(self._meta['collection_status'])

        """
        partitions: Dict
        """
        self._partitions = {}
        if 'partitions' in self._meta and isinstance(self._meta['partitions'], dict):
            for partition_name, partition_meta in self._meta['partitions'].items():
                self._partitions[partition_name] = PartitionMetaBuilder.from_meta(partition_name=partition_name,
                                                                                  partition_meta=partition_meta)

    @property
    def name(self):
        return self._name

    @property
    def dimension(self):
        return self._dimension

    @property
    def dtype(self):
        return self._dtype

    @property
    def metric(self):
        return self._metric

    @property
    def vector_field(self):
        return self._vector_field

    @property
    def fields(self):
        return self._fields

    def field(self, idx: Union[int, str]):
        if isinstance(idx, int):
            if idx < 0 or idx >= self._fields_len:
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f"DashVectorSDK Collection Fields Index({idx}) is Invalid and nd must be in [0, {idx}]")
            return self._fields[idx]

        if isinstance(idx, str):
            for field in self._fields:
                if field.field_name == idx:
                    return field
            raise DashVectorException(code=DashVectorCode.NotFound,
                                   reason=f"DashVectorSDK Collection Field Index({idx}) not Found.")

        raise DashVectorException(code=DashVectorCode.InvalidArgument,
                               reason=f"DashVectorSDK Collection Field Index Type({type(idx)}) is Invalid")

    @property
    def state(self):
        return self._state

    @property
    def partitions(self):
        return self._partitions

    def __dict__(self):
        meta_dict = {
            'name': self.name,
            'dimension': self.dimension,
            'dtype': DataType.str(self.dtype),
            'metric': self.metric
        }

        if self.state is not None:
            meta_dict['state'] = CollectionStatus.str(self.state)

        if self.fields is not None:
            meta_dict['fields'] = []
            for field in self.fields:
                meta_dict['fields'].append(field.__dict__())

        if self.partitions is not None:
            meta_dict['partitions'] = {}
            for partition_name, partition_meta in self.partitions.items():
                meta_dict['partitions'][partition_name] = partition_meta.__dict__()

        return meta_dict

    def __str__(self):
        return json.dumps(self.__dict__())

    def __repr__(self):
        return self.__str__()


class CollectionStats(object):
    def __init__(self,
                 *,
                 stats: Dict):
        """
        stats: Dict
        """
        self._stats = stats
        if not isinstance(stats, dict):
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason="DashVectorSDK Collection Stats is Invalid")

        """
        total_doc_count: int
        """
        self._total_doc_count = 0

        """
        total_segment_count: int
        """
        self._total_segment_count = 0

        """
        total_index_file_count: int
        """
        self._total_index_file_count = 0

        """
        total_index_file_size: int
        """
        self._total_index_file_size = 0

        """
        total_delete_doc_count: int
        """
        self._total_delete_doc_count = 0

        """
        index_completeness: float
        """
        self._index_completeness = 1.0

        """
        partitions: Dict
        """
        self._partitions = {}
        if 'partitions' not in self._stats or not isinstance(self._stats['partitions'], dict):
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason="DashVectorSDK Collection Stats is Invalid")

        for partition_name, partition_meta in self._stats['partitions'].items():
            self._partitions[partition_name] = PartitionStatsBuilder.from_meta(partition_name, partition_meta)
            self._total_doc_count += self._partitions[partition_name].total_doc_count
            self._total_segment_count += self._partitions[partition_name].total_segment_count
            self._total_index_file_count += self._partitions[partition_name].total_index_file_count
            self._total_index_file_size += self._partitions[partition_name].total_index_file_size
            self._total_delete_doc_count += self._partitions[partition_name].total_delete_doc_count

        if 'index_completeness' in self._stats and isinstance(self._stats['index_completeness'], float):
            self._index_completeness = self._stats['index_completeness']

    @property
    def total_doc_count(self):
        return self._total_doc_count

    @property
    def total_segment_count(self):
        return self._total_segment_count

    @property
    def total_index_file_count(self):
        return self._total_index_file_count

    @property
    def total_index_file_size(self):
        return self._total_index_file_size

    @property
    def total_delete_doc_count(self):
        return self._total_delete_doc_count

    @property
    def index_completeness(self):
        return self._index_completeness

    @property
    def partitions(self):
        return self._partitions

    def __dict__(self):
        meta_dict = {
            'total_doc_count': self.total_doc_count,
            'total_segment_count': self.total_segment_count,
            'total_index_file_count': self.total_index_file_count,
            'total_index_file_size': self.total_index_file_size,
            'total_delete_doc_count:': self.total_delete_doc_count,
            'index_completeness': self.index_completeness
        }

        partition_dict = {}
        for partition_name, partition_meta in self._partitions.items():
            partition_dict[partition_name] = partition_meta.__dict__()
        meta_dict['partitions'] = partition_dict
        
        return meta_dict

    def __str__(self):
        return json.dumps(self.__dict__())

    def __repr__(self):
        return self.__str__()


class DashVectorResponse(object):
    def __init__(self,
                 response: Optional[RPCResponse] = None,
                 *,
                 exception: Optional[DashVectorException] = None):

        self._code = DashVectorCode.Unknown
        self._message = ""
        self._output = None
        self.__response = response
        self.__exception = exception

        if self.__response is None:
            self._code = DashVectorCode.Success

        if self.__response is not None and not self.__response.async_req:
            self.get()

        if self.__exception is not None:
            self._code = self.__exception.code
            self._message = self.__exception.message

    def get(self):
        if self._code != DashVectorCode.Unknown:
            return self

        if self.__response is None:
            return self

        try:
            self._code = DashVectorCode.Success
            self._output = self.__response.get()
        except DashVectorException as e:
            self._code = e.code
            self._message = e.message

        return self

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._message

    @property
    def request_id(self):
        if self.__response is not None:
            return self.__response.get_request_id()
        if self.__exception is not None:
            return self.__exception.request_id
        return ""

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, value: Any):
        self._output = value

    @property
    def response(self):
        return self.__response

    def __dict__(self):
        if self._output is None:
            return {
                'code': self.code,
                'message': self.message,
                'requests_id': self.request_id
            }
        elif isinstance(self._output, (str, int, float)):
            return {
                'code': self.code,
                'message': self.message,
                'requests_id': self.request_id,
                'output': str(self._output)
            }
        elif isinstance(self._output, list):
            output_list = []
            for output_value in self._output:
                if isinstance(output_value, (str, int, float)):
                    output_list.append(str(output_value))
                elif hasattr(output_value, "__dict__"):
                    output_list.append(output_value.__dict__())
                elif hasattr(output_value, "__str__"):
                    output_list.append(output_value.__str__())
                else:
                    output_list.append(str(type(output_value)))
            return {
                'code': self.code,
                'message': self.message,
                'requests_id': self.request_id,
                'output': output_list
            }
        elif isinstance(self._output, dict):
            output_dict = {}
            for output_key, output_value in self._output.items():
                if isinstance(output_value, (str, int, float)):
                    output_dict[output_key] = str(output_value)
                elif hasattr(output_value, "__dict__"):
                    output_dict[output_key] = output_value.__dict__()
                elif hasattr(output_value, "__str__"):
                    output_dict[output_key] = output_value.__str__()
                else:
                    output_dict[output_key] = str(type(output_value))
            return {
                'code': self.code,
                'message': self.message,
                'requests_id': self.request_id,
                'output': output_dict
            }
        elif hasattr(self._output, "__dict__"):
            return {
                'code': self.code,
                'message': self.message,
                'requests_id': self.request_id,
                'output': self._output.__dict__()
            }
        elif hasattr(self._output, "__str__"):
            return {
                'code': self.code,
                'message': self.message,
                'requests_id': self.request_id,
                'output': self._output.__str__()
            }
        else:
            return {
                'code': self.code,
                'message': self.message,
                'requests_id': self.request_id,
                'output': str(type(self._output))
            }

    def __str__(self):
        return json.dumps(self.__dict__())

    def __repr__(self):
        return self.__str__()

    def __bool__(self):
        return self.code == DashVectorCode.Success

    def __len__(self):
        return len(self._output)

    def __iter__(self):
        return self._output.__iter__()

    def __contains__(self, item):
        if hasattr(self._output, "__contains__"):
            return self.output.__contains__(item)
        else:
            raise TypeError(f"argument of type '{type(self.output)}' is not iterable")

    def __getitem__(self, item):
        if hasattr(self._output, "__getitem__"):
            return self.output.__getitem__(item)
        else:
            raise TypeError(f"'{type(self.output)}' object is not subscriptable")


class DataParser:
    data_type_to_dimension = {
        DataType.VECTOR_BINARY32: 32,
        DataType.VECTOR_BINARY64: 64,
    }

    data_type_to_format = {
        DataType.VECTOR_FP16: 'e',
        DataType.VECTOR_FP32: 'f',
        DataType.VECTOR_FP64: 'd',
        DataType.VECTOR_INT16: 'h',
        DataType.VECTOR_INT8: 'c',
        DataType.VECTOR_BINARY32: 'I',
        DataType.VECTOR_BINARY64: 'Q',
    }

    @staticmethod
    def parse_pb_fields(pb_fields):
        res = {}
        for field in pb_fields:
            if not field.value.HasField('value_oneof'):
                continue
            attr_name = field.value.WhichOneof('value_oneof')
            res[field.name] = getattr(field.value, attr_name)
        return res

    @staticmethod
    def parse_vector_data_type(dtype):
        if isinstance(dtype, DataType):
            if dtype < DataType.VECTOR_BINARY32:
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f'Invalid vector data type {dtype}')
            return dtype
        if dtype in _vector_dtype_map:
            return _vector_dtype_map[dtype]
        raise DashVectorException(code=DashVectorCode.InvalidArgument,
                               reason=f'Invalid vector data type {dtype}')

    @staticmethod
    def parse_attr_data_type(dtype):
        if isinstance(dtype, DataType):
            if dtype >= DataType.VECTOR_BINARY32:
                raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                       reason=f'Invalid attribute data type {dtype}')
            return dtype
        if dtype in _attr_dtype_map:
            return _attr_dtype_map[dtype]
        raise DashVectorException(code=DashVectorCode.InvalidArgument,
                               reason=f'Invalid attribute data type {dtype}')

    @staticmethod
    def pack_feature(feature, data_type, dimension):
        format_dimension = dimension // DataParser.data_type_to_dimension.get(data_type, 1)
        if data_type not in DataParser.data_type_to_format:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK not support auto pack feature type[{data_type}]")
        return struct.pack(f'<{format_dimension}{DataParser.data_type_to_format[data_type]}', *feature)

    @staticmethod
    def unpack_feature(feature, data_type, dimension):
        format_dimension = dimension // DataParser.data_type_to_dimension.get(data_type, 1)

        if data_type not in DataParser.data_type_to_format:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK not support auto pack feature type[{data_type}]")
        return struct.unpack(f'<{format_dimension}{DataParser.data_type_to_format[data_type]}', feature)
