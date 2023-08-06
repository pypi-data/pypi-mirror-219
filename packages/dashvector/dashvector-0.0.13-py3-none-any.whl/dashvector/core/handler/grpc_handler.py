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

import json
import grpc
from google.protobuf.json_format import MessageToJson

from dashvector.common.error import DashVectorCode, DashVectorException, DashVectorGRPCException
from dashvector.common.status import PartitionStatus
from dashvector.common.handler import RPCHandler, RPCResponse

from dashvector.core.proto import centaur_pb2_grpc
from dashvector.core.models.create_collection_request import CreateCollectionRequest
from dashvector.core.models.describe_collection_request import DescribeCollectionRequest
from dashvector.core.models.list_collection_request import ListCollectionRequest
from dashvector.core.models.stats_collection_request import StatsCollectionRequest
from dashvector.core.models.drop_collection_request import DropCollectionRequest
from dashvector.core.models.get_version_request import GetVersionRequest
from dashvector.core.models.upsert_doc_request import UpsertDocRequest
from dashvector.core.models.delete_doc_request import DeleteDocRequest
from dashvector.core.models.get_doc_request import GetDocRequest
from dashvector.core.models.query_doc_request import QueryDocRequest
from dashvector.core.models.create_partition_request import CreatePartitionRequest
from dashvector.core.models.drop_partition_request import DropPartitionRequest
from dashvector.core.doc import DocBuilder

from dashvector.version import __version__


class GRPCHandler(RPCHandler):
    def __init__(self, *,
                 endpoint: str,
                 api_key: str = "",
                 timeout: float = 10.0):

        """
        endpoint: str
        """
        if not isinstance(endpoint, str):
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK GRPCHandler endpoint Type({endpoint}) is Invalid")

        if len(endpoint) <= 0:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK GRPCHandler endpoint Empty")

        """
        api_key: str
        """
        if not isinstance(api_key, str):
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK GRPCHandler api_key Type({api_key}) is Invalid")

        """
        timeout: float
        """
        if isinstance(timeout, float):
            pass
        elif isinstance(timeout, int):
            timeout = float(timeout)
        else:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK GRPCHandler timeout Type({timeout}) is Invalid")
        if timeout <= 0.000001:
            timeout = 365.5 * 86400

        super().__init__(endpoint=endpoint,
                         api_key=api_key,
                         timeout=timeout)

        self._channel = grpc.insecure_channel(self._endpoint)
        self._stub = centaur_pb2_grpc.CentaurServiceStub(self._channel)
        self._metadata = (("dashvector-auth-token", self._api_key), ("dashvertor-client-version", __version__))

    @classmethod
    def _parse_request_id_from_exception(cls, e: grpc.RpcError):
        for metak, metav in e.trailing_metadata():
            if metak == "request-id":
                return metav
        return ""

    class _GRPCResponse(RPCResponse):
        def __init__(self,
                     future,
                     *,
                     req=None,
                     async_req=False,
                     attr_name=None):

            super().__init__(async_req=async_req)
            self._future = future
            self._attr_name = attr_name
            self._request = req
            self._response = None

        def get(self):
            if self._response is None:
                try:
                    self._response = self._parse_response(self._future.result(),
                                                          attr_name=self._attr_name)
                except grpc.RpcError as e:
                    raise DashVectorGRPCException(code=e.code(),
                                               reason=e.details(),
                                               request_id=GRPCHandler._parse_request_id_from_exception(e))

            if self._response is None:
                return None

            if self._attr_name == "docs":
                if isinstance(self._request, GetDocRequest):
                    rsp_doc_dict = {}
                    out_doc_dict = {}
                    for rsp_doc in self._response:
                        if 'pk' not in rsp_doc:
                            continue
                        rsp_doc_dict[rsp_doc['pk']] = rsp_doc

                    for request_id in self._request.ids:
                        _id_str = str(request_id)
                        if _id_str not in rsp_doc_dict:
                            continue
                        out_doc_dict[request_id] = DocBuilder.from_meta(doc_meta=rsp_doc_dict[_id_str],
                                                                        collection_meta=self._request.collection_meta,
                                                                        include_vector=self._request.include_vector,
                                                                        id_is_int=isinstance(request_id, int))
                    return out_doc_dict
                else:
                    out_doc_dict = {}
                    for rsp_doc in self._response:
                        if 'pk' not in rsp_doc:
                            continue
                        out_doc_dict[rsp_doc['pk']] = DocBuilder.from_meta(rsp_doc)
                    return out_doc_dict
            if self._attr_name == "doc_results":
                doc_meta_list = []
                for rsp_docs in self._response:
                    if 'docs' not in rsp_docs:
                        continue
                    for rsp_per_doc in rsp_docs['docs']:
                        if isinstance(self._request, QueryDocRequest):
                            per_doc_meta = DocBuilder.from_meta(rsp_per_doc,
                                                                collection_meta=self._request.collection_meta,
                                                                include_vector=self._request.include_vector)
                        else:
                            per_doc_meta = DocBuilder.from_meta(rsp_per_doc)
                        doc_meta_list.append(per_doc_meta)
                return doc_meta_list
            if self._attr_name == 'partition_status':
                return PartitionStatus.get(self._response)
            if self._attr_name == 'has_partition':
                return self._response if isinstance(self._response, bool) else False
            if self._attr_name == 'list_partition':
                if not isinstance(self._response, dict):
                    return []
                partition_list = []
                for partition_key, partition_value in self._response.items():
                    partition_list.append(partition_key)
                return partition_list
            return self._response

        def get_request_id(self):
            if self._request_id is not None:
                return self._request_id

            self._request_id = ""
            for meta_k, meta_v in self._future.trailing_metadata():
                if meta_k == "request-id":
                    self._request_id = meta_v
                    break
            return self._request_id

        @property
        def request_id(self):
            return self.get_request_id()

        def _parse_response(self, pb, attr_name=None):
            if pb.status.code != 0:
                raise DashVectorException(pb.status.code, pb.status.reason)

            if attr_name is None:
                return None

            pb_to_json = json.loads(MessageToJson(pb, including_default_value_fields=True, preserving_proto_field_name=True))
            if attr_name == "doc":
                return pb_to_json["docs"] if 'docs' in pb_to_json else []
            if attr_name == 'has_partition':
                return True if 'partition_status' in pb_to_json else False
            if attr_name == 'list_partition':
                return pb_to_json['collection']['partitions'] if 'collection' in pb_to_json and 'partitions' in pb_to_json['collection'] else {}
            if attr_name not in pb_to_json:
                return None
            return pb_to_json[attr_name]

    def create_collection(self,
                          create_request: CreateCollectionRequest,
                          *,
                          async_req: bool = False) -> RPCResponse:
        try:
            rebuild_timeout = self._timeout
            if rebuild_timeout < 30.0:
                rebuild_timeout = 30.0
            rsp = self._stub.create_collection.future(create_request.to_proto(),
                                                      metadata=self._metadata,
                                                      timeout=rebuild_timeout)
            return self._GRPCResponse(rsp, async_req=async_req)
        except grpc.RpcError as e:
            raise DashVectorGRPCException(code=e.code(),
                                       reason=e.details(),
                                       request_id=self._parse_request_id_from_exception(e))

    def drop_collection(self,
                        drop_request: DropCollectionRequest,
                        *,
                        async_req: bool = False) -> RPCResponse:
        try:
            rebuild_timeout = self._timeout
            if rebuild_timeout < 30.0:
                rebuild_timeout = 30.0
            rsp = self._stub.drop_collection.future(drop_request.to_proto(),
                                                    metadata=self._metadata,
                                                    timeout=rebuild_timeout)
            return self._GRPCResponse(rsp, async_req=async_req)
        except grpc.RpcError as e:
            raise DashVectorGRPCException(code=e.code(),
                                       reason=e.details(),
                                       request_id=self._parse_request_id_from_exception(e))

    def describe_collection(self,
                            describe_request: DescribeCollectionRequest,
                            *,
                            async_req: bool = False) -> RPCResponse:
        try:
            rsp = self._stub.describe_collection.future(describe_request.to_proto(),
                                                        metadata=self._metadata,
                                                        timeout=self._timeout)
            return self._GRPCResponse(rsp, async_req=async_req, attr_name='collection')
        except grpc.RpcError as e:
            raise DashVectorGRPCException(code=e.code(),
                                       reason=e.details(),
                                       request_id=self._parse_request_id_from_exception(e))

    def list_collections(self,
                         *,
                         async_req: bool = False) -> RPCResponse:
        try:
            rsp = self._stub.list_collections.future(ListCollectionRequest().to_proto(),
                                                     metadata=self._metadata,
                                                     timeout=self._timeout)
            return self._GRPCResponse(rsp, async_req=async_req, attr_name="collections")
        except grpc.RpcError as e:
            raise DashVectorGRPCException(code=e.code(),
                                       reason=e.details(),
                                       request_id=self._parse_request_id_from_exception(e))

    def stats_collection(self,
                         stats_request: StatsCollectionRequest,
                         *,
                         async_req: bool = False) -> RPCResponse:
        try:
            rsp = self._stub.stats_collection.future(stats_request.to_proto(),
                                                     metadata=self._metadata,
                                                     timeout=self._timeout)
            return self._GRPCResponse(rsp, async_req=async_req, attr_name="collection_stats")
        except grpc.RpcError as e:
            raise DashVectorGRPCException(code=e.code(),
                                       reason=e.details(),
                                       request_id=self._parse_request_id_from_exception(e))

    def get_version(self,
                    *,
                    async_req: bool = False) -> RPCResponse:
        try:
            rsp = self._stub.get_version.future(GetVersionRequest().to_proto(),
                                                metadata=self._metadata,
                                                timeout=self._timeout)
            return self._GRPCResponse(rsp, async_req=async_req, attr_name="version")
        except grpc.RpcError as e:
            raise DashVectorGRPCException(code=e.code(),
                                       reason=e.details(),
                                       request_id=self._parse_request_id_from_exception(e))

    def collection_insert_doc(self,
                              insert_request: UpsertDocRequest,
                              *,
                              async_req: bool = False) -> RPCResponse:
        try:
            rsp = self._stub.insert_doc.future(insert_request.to_proto(),
                                               metadata=self._metadata,
                                               timeout=self._timeout)
            return self._GRPCResponse(rsp, async_req=async_req)
        except grpc.RpcError as e:
            raise DashVectorGRPCException(code=e.code(),
                                       reason=e.details(),
                                       request_id=self._parse_request_id_from_exception(e))

    def collection_update_doc(self,
                              update_request: UpsertDocRequest,
                              *,
                              async_req: bool = False) -> RPCResponse:
        try:
            rsp = self._stub.update_doc.future(update_request.to_proto(),
                                               metadata=self._metadata,
                                               timeout=self._timeout)
            return self._GRPCResponse(rsp, async_req=async_req)
        except grpc.RpcError as e:
            raise DashVectorGRPCException(code=e.code(),
                                       reason=e.details(),
                                       request_id=self._parse_request_id_from_exception(e))

    def collection_upsert_doc(self,
                              upsert_request: UpsertDocRequest,
                              *,
                              async_req: bool = False) -> RPCResponse:
        try:
            rsp = self._stub.upsert_doc.future(upsert_request.to_proto(),
                                               metadata=self._metadata,
                                               timeout=self._timeout)
            return self._GRPCResponse(rsp, async_req=async_req)
        except grpc.RpcError as e:
            raise DashVectorGRPCException(code=e.code(),
                                       reason=e.details(),
                                       request_id=self._parse_request_id_from_exception(e))

    def collection_delete_doc(self,
                              delete_request: DeleteDocRequest,
                              *,
                              async_req: bool = False) -> RPCResponse:
        try:
            rsp = self._stub.delete_doc.future(delete_request.to_proto(),
                                               metadata=self._metadata,
                                               timeout=self._timeout)
            return self._GRPCResponse(rsp, async_req=async_req)
        except grpc.RpcError as e:
            raise DashVectorGRPCException(code=e.code(),
                                       reason=e.details(),
                                       request_id=self._parse_request_id_from_exception(e))

    def collection_get_doc_by_key(self,
                                  get_request: GetDocRequest,
                                  *,
                                  async_req: bool = False) -> RPCResponse:
        try:
            rsp = self._stub.get_doc_by_key.future(get_request.to_proto(),
                                                   metadata=self._metadata,
                                                   timeout=self._timeout)
            return self._GRPCResponse(rsp, req=get_request,
                                      async_req=async_req, attr_name="docs")
        except grpc.RpcError as e:
            raise DashVectorGRPCException(code=e.code(),
                                       reason=e.details(),
                                       request_id=self._parse_request_id_from_exception(e))

    def collection_query_doc(self,
                             query_request: QueryDocRequest,
                             *,
                             async_req: bool = False) -> RPCResponse:
        try:
            rsp = self._stub.query.future(query_request.to_proto(),
                                          metadata=self._metadata,
                                          timeout=self._timeout)
            return self._GRPCResponse(rsp, req=query_request,
                                      attr_name="doc_results",
                                      async_req=async_req)
        except grpc.RpcError as e:
            raise DashVectorGRPCException(code=e.code(),
                                       reason=e.details(),
                                       request_id=self._parse_request_id_from_exception(e))

    def collection_create_partition(self,
                                    create_request: CreatePartitionRequest,
                                    *,
                                    async_req: bool = False) -> RPCResponse:
        try:
            rsp = self._stub.create_partition.future(create_request.to_proto(),
                                                     metadata=self._metadata,
                                                     timeout=self._timeout)
            return self._GRPCResponse(rsp, async_req=async_req)
        except grpc.RpcError as e:
            raise DashVectorGRPCException(code=e.code(),
                                       reason=e.details(),
                                       request_id=self._parse_request_id_from_exception(e))

    def collection_drop_partition(self,
                                  drop_request: DropPartitionRequest,
                                  *,
                                  async_req: bool = False) -> RPCResponse:
        try:
            rsp = self._stub.drop_partition.future(drop_request.to_proto(),
                                                   metadata=self._metadata,
                                                   timeout=self._timeout)
            return self._GRPCResponse(rsp, async_req=async_req)
        except grpc.RpcError as e:
            raise DashVectorGRPCException(code=e.code(),
                                       reason=e.details(),
                                       request_id=self._parse_request_id_from_exception(e))

    def close(self) -> None:
        self._channel.close()
        return None
