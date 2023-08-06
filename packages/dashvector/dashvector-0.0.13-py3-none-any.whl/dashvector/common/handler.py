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

from abc import abstractmethod
from google.protobuf.message import Message
from google.protobuf.json_format import MessageToJson
from dashvector.common.error import DashVectorCode, DashVectorException


class RPCRequest(object):
    def __init__(self, *, request: Message):
        self.request = request
        self.request_str = request.SerializeToString()
        self.request_len = len(self.request_str)
        if self.request_len > (2 * 1024 * 1024):
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK Request Length({self.request_len}) exceeds Maximum Length(2MiB) Limit")

    def to_json(self):
        return MessageToJson(self.request, including_default_value_fields=True)

    def to_proto(self):
        return self.request

    def to_string(self):
        return self.request_str


class RPCResponse(object):
    def __init__(self, *, async_req):
        self._async_req = async_req
        self._request_id = None

    @property
    def async_req(self):
        return self._async_req

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def get_request_id(self):
        pass


class RPCHandler(object):
    def __init__(self, *,
                 endpoint: str,
                 api_key: str = "",
                 timeout: float = 10.0):
        self._endpoint = endpoint
        self._api_key = api_key
        self._timeout = timeout

    @abstractmethod
    def create_collection(self,
                          create_request,
                          *,
                          async_req=False) -> RPCResponse:
        pass

    @abstractmethod
    def drop_collection(self,
                        drop_request,
                        *,
                        async_req=False) -> RPCResponse:
        pass

    @abstractmethod
    def describe_collection(self,
                            describe_request,
                            *,
                            async_req=False) -> RPCResponse:
        pass

    def list_collections(self,
                         *,
                         async_req=False) -> RPCResponse:
        pass

    @abstractmethod
    def stats_collection(self,
                         stats_request,
                         *,
                         async_req=False) -> RPCResponse:
        pass

    @abstractmethod
    def get_version(self,
                    *,
                    async_req) -> RPCResponse:
        pass

    @abstractmethod
    def collection_insert_doc(self,
                              insert_request,
                              *,
                              async_req=False) -> RPCResponse:
        pass

    @abstractmethod
    def collection_update_doc(self,
                              update_request,
                              *,
                              async_req=False) -> RPCResponse:
        pass

    @abstractmethod
    def collection_upsert_doc(self,
                              upsert_request,
                              *,
                              async_req=False) -> RPCResponse:
        pass

    @abstractmethod
    def collection_delete_doc(self,
                              delete_request,
                              *,
                              async_req=False) -> RPCResponse:
        pass

    @abstractmethod
    def collection_get_doc_by_key(self,
                                  get_request,
                                  *,
                                  async_req=False) -> RPCResponse:
        pass

    @abstractmethod
    def collection_query_doc(self,
                             query_request,
                             *,
                             async_req=False) -> RPCResponse:
        pass

    @abstractmethod
    def collection_create_partition(self,
                                    create_request,
                                    *,
                                    async_req=False) -> RPCResponse:
        pass

    @abstractmethod
    def collection_drop_partition(self,
                                  drop_partition,
                                  *,
                                  async_req=False) -> RPCResponse:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

