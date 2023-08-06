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

import numpy as np
from typing import List, Dict, Tuple, Union, Optional
from dashvector.common.error import DashVectorException
from dashvector.common.types import DashVectorCode, DashVectorResponse
from dashvector.common.types import CollectionMeta, CollectionStats
from dashvector.common.handler import RPCHandler, RPCResponse
from dashvector.core.models.describe_collection_request import DescribeCollectionRequest
from dashvector.core.models.upsert_doc_request import UpsertDocRequest
from dashvector.core.models.delete_doc_request import DeleteDocRequest
from dashvector.core.models.get_doc_request import GetDocRequest
from dashvector.core.models.query_doc_request import QueryDocRequest
from dashvector.core.models.create_partition_request import CreatePartitionRequest
from dashvector.core.models.drop_partition_request import DropPartitionRequest
from dashvector.core.models.stats_collection_request import StatsCollectionRequest
from dashvector.core.doc import Doc

__all__ = ["Collection"]


class Collection(DashVectorResponse):

    """
    A Client for Doc and Partition Operations in a Collection
    """
    def insert(self,
               docs: Union[Doc, List[Doc], Tuple, List[Tuple]],
               *,
               partition: Optional[str] = None,
               async_req: bool = False) -> DashVectorResponse:

        """
        Insert one or more Docs.

        Args:
            docs (Union[Doc, List[Doc], Tuple, List[Tuple]]): one or more Docs which will insert into collection.
            partition (str): a partition name in collection. [optional]
            async_req (bool): use asynchronous operation.

        Return:
            DashVectorResponse, include code / message / request_id and a get() method,
                             code == DashVectorCode.Success means insert docs success, otherwise means failure.
                             if you use async_req, must call get() method first.

        Examples:
            [insert]
            rsp = collection.insert(("a", [0.1, 0.2], {'price': 100, 'type': "dress"}))
            if not rsp:
                raise RuntimeError(f"InsertDoc Failed, error:{rsp.code}, message:{rsp.message}")

            [insert with numpy]
            rsp = collection.insert(("a", np.array([0.1, 0.2], {'price': 100, 'type': "dress"}))
            if not rsp:
                raise RuntimeError(f"InsertDoc Failed, error:{rsp.code}, message:{rsp.message}")

            [insert with doc]
            rsp = collection.insert(Doc(id="a", vector=[0.1, 0.2], fields={'price': 100, 'type': "dress"}))
            if not rsp:
                raise RuntimeError(f"InsertDoc Failed, error:{rsp.code}, message:{rsp.message}")

            [batch insert]
            rsp = collection.insert([("a", [0.1, 0.2], {'price': 100, 'type': "dress"}), ("b", [0.3, 0.4], {'price': 80, 'type': "shirt"})])
            if not rsp:
                raise RuntimeError(f"InsertDoc Failed, error:{rsp.code}, message:{rsp.message}")

            [batch insert with doc]
            rsp = collection.insert([Doc(id="a", vector=[0.1, 0.2], fields={'price': 100, 'type': "dress"}), vector=Doc(id="b", [0.3, 0.4], fields={'price': 80, 'type': "shirt"})])
            if not rsp:
                raise RuntimeError(f"InsertDoc Failed, error:{rsp.code}, message:{rsp.message}")

            [asynchronous insert]
            rsp = collection.insert(("a", [0.1, 0.2], {'price': 100, 'type': "dress"}), async_req=True)
            if not rsp.get():
                raise RuntimeError(f"InsertDoc Failed, error:{rsp.code}, message:{rsp.message}")

            [asynchronous batch insert]
            rsp = collection.insert([("a", [0.1, 0.2], {'price': 100, 'type': "dress"}), ("b", [0.3, 0.4], {'price': 80, 'type': "shirt"})], async_req=True)
            if not rsp.get():
                raise RuntimeError(f"InsertDoc Failed, error:{rsp.code}, message:{rsp.message}")
        """

        if self._code != DashVectorCode.Success:
            return DashVectorResponse(None,
                                   exception=DashVectorException(code=DashVectorCode.RuntimeError,
                                                              reason="DashVectorSDK Collection initialize Failed",
                                                              request_id=self.request_id))

        try:
            insert_request = UpsertDocRequest(collection_meta=self._collection_meta,
                                              docs=docs,
                                              partition=partition,
                                              action="insert")
        except DashVectorException as e:
            return DashVectorResponse(None, exception=e)

        return DashVectorResponse(self._handler.collection_insert_doc(insert_request, async_req=async_req))

    def update(self,
               docs: Union[Doc, List[Doc], Tuple, List[Tuple]],
               *,
               partition: Optional[str] = None,
               async_req: bool = False) -> DashVectorResponse:

        """
        Update one or more Docs like Insert Operation.

        Args:
            docs (Union[Doc, List[Doc], Tuple, List[Tuple]]): one or more Docs which will insert into collection.
            partition (str): a partition name in collection. [optional]
            async_req (bool): use asynchronous operation.

        Return:
            DashVectorResponse, include code / message / request_id and a get() method,
                             code == DashVectorCode.Success means update docs success, otherwise means failure.
                             if you use async_req, must call get() method first.
        """

        if self._code != DashVectorCode.Success:
            return DashVectorResponse(None,
                                   exception=DashVectorException(code=DashVectorCode.RuntimeError,
                                                              reason="DashVectorSDK Collection initialize Failed",
                                                              request_id=self.request_id))

        try:
            update_request = UpsertDocRequest(collection_meta=self._collection_meta,
                                              docs=docs,
                                              partition=partition,
                                              action="update")
        except DashVectorException as e:
            return DashVectorResponse(None, exception=e)

        return DashVectorResponse(self._handler.collection_update_doc(update_request, async_req=async_req))

    def upsert(self,
               docs: Union[Doc, List[Doc], Tuple, List[Tuple]],
               *,
               partition: Optional[str] = None,
               async_req: bool = False) -> DashVectorResponse:

        """
        Update one or more Docs and do Insert Operation when Doc does not exist.

        Args:
            docs (Union[Doc, List[Doc], Tuple, List[Tuple]]): one or more docs which will update into collection.
            partition (str): a partition name in collection. [optional]
            async_req (bool): use asynchronous operation.

        Return:
            DashVectorResponse, include code / message / request_id and a get() method,
                             code == DashVectorCode.Success means update docs success, otherwise means failure.
                             if you use async_req, must call get() method first.
        """

        if self._code != DashVectorCode.Success:
            return DashVectorResponse(None,
                                   exception=DashVectorException(code=DashVectorCode.RuntimeError,
                                                              reason="DashVectorSDK Collection initialize Failed",
                                                              request_id=self.request_id))

        try:
            upsert_request = UpsertDocRequest(collection_meta=self._collection_meta,
                                              docs=docs,
                                              partition=partition,
                                              action="upsert")
        except DashVectorException as e:
            return DashVectorResponse(None, exception=e)

        return DashVectorResponse(self._handler.collection_upsert_doc(upsert_request, async_req=async_req))

    def fetch(self,
              ids: Union[Union[str, int], List[Union[str, int]]],
              *,
              partition: Optional[str] = None,
              async_req: bool = False) -> DashVectorResponse:

        """
        Get one or more Docs with ids(primary keys).

        Args:
           ids (Union[Union[str, int], List[Union[str, int]]]): one or more docs primary keys.
           partition (str): a partition name in collection. [optional]
           async_req (bool): use asynchronous operation.

        Return:
           DashVectorResponse, include code / message / request_id / output and a get() method,
                            code == DashVectorCode.Success means fetch docs success, otherwise means failure.
                            if you use async_req, must call get() method first.

        Examples:
            [fetch a Doc]
            rsp = collection.fetch(ids="primary_key")
            if not rsp:
                raise RuntimeError(f"FetchDoc Failed, error:{rsp.code}, message:{rsp.message}")
            doc_meta = rsp.output
            print("doc_meta:", doc_meta)

            [fetch multiple Docs]
            rsp = collection.fetch(ids=["primary_key_1", "primary_key_2", "primary_key_3"])
            if not rsp:
                raise RuntimeError(f"FetchDoc Failed, error:{rsp.code}, message:{rsp.message}")
            doc_metas = rsp.output
            for doc_meta in doc_metas:
                print("doc_meta:", doc_meta)

            [asynchronous fetch a Doc]
            rsp = collection.fetch(ids="primary_key", async_req=True)
            if rsp.get().code != DashVectorCode.Success:
                raise RuntimeError(f"FetchDoc Failed, error:{rsp.code}, message:{rsp.message}")
            doc_meta = rsp.output
            print("doc_meta:", doc_meta)
        """

        if self._code != DashVectorCode.Success:
            return DashVectorResponse(None,
                                   exception=DashVectorException(code=DashVectorCode.RuntimeError,
                                                              reason="DashVectorSDK Collection initialize Failed",
                                                              request_id=self.request_id))

        try:
            get_request = GetDocRequest(collection_meta=self._collection_meta,
                                        ids=ids,
                                        partition=partition)
        except DashVectorException as e:
            return DashVectorResponse(None, exception=e)

        return DashVectorResponse(self._handler.collection_get_doc_by_key(get_request, async_req=async_req))

    def query(self,
              vector: Union[List[Union[int, float]], np.ndarray],
              *,
              topk: int = 10,
              filter: Optional[str] = None,
              include_vector: bool = False,
              partition: Optional[str] = None,
              output_fields: Optional[List[str]] = None,
              async_req: bool = False) -> DashVectorResponse:

        """
        Query Docs with a vector.

        Args:
            vector (Union[List[Union[int, float, bool]], np.ndarray]): a doc vector.
            topk (int): return topk similarity docs, default is 10.
            filter (Optional[str]): doc fields filter conditions that meet the SQL where clause specification. [optional]
            include_vector (bool): whether to has vector in return docs, default is False.
            partition (str): a partition name in collection. [optional]
            output_fields (Optional[List[str]]): select fields in return docs. [optional]
            async_req (bool): use asynchronous operation, default is False.

        Return:
            DashVectorResponse, include code / message / request_id / output and a get() method,
                             code == DashVectorCode.Success means query docs success, otherwise means failure.
                             if you use async_req, must call get() method first.

        Examples:
            [query]
            rsp = collection.query([0.1, 0.2])
            if not rsp:
                raise RuntimeError(f"Query Failed, error:{rsp.code}, message:{rsp.message}")
            doc_metas = rsp.output
            for doc_meta in doc_metas:
                print("doc_meta:", doc_meta)

            [query with topk]
            rsp = collection.query([0.1, 0.2], topk=100")
            if not rsp:
                raise RuntimeError(f"Query Failed, error:{rsp.code}, message:{rsp.message}")
            doc_metas = rsp.output
            for doc_meta in doc_metas:
                print("doc_meta:", doc_meta)

            [query with filter]
            rsp = collection.query([0.1, 0.2], topk=100, filter="price > 99")
            if not rsp:
                raise RuntimeError(f"Query Failed, error:{rsp.code}, message:{rsp.message}")
            doc_metas = rsp.output
            for doc_meta in doc_metas:
                print("doc_meta:", doc_meta)

            [query with output_fields]
            rsp = collection.query([0.1, 0.2], topk=100, output_fields=["price"],)
            if not rsp:
                raise RuntimeError(f"Query Failed, error:{rsp.code}, message:{rsp.message}")
            doc_metas = rsp.output
            for doc_meta in doc_metas:
                print("doc_meta:", doc_meta)

            [query with include_vector]
            rsp = collection.query([0.1, 0.2], topk=100, output_fields=["price"], include_vector=True)
            if not rsp:
                raise RuntimeError(f"Query Failed, error:{rsp.code}, message:{rsp.message}")
            doc_metas = rsp.output
            for doc_meta in doc_metas:
                print("doc_meta:", doc_meta)

            [asynchronous query]
            rsp = collection.query([0.1, 0.2], async_req=True)
            if rsp.get().code != DashVectorCode.Success:
                raise RuntimeError(f"Query Failed, error:{rsp.code}, message:{rsp.message}")
            doc_metas = rsp.output
            for doc_meta in doc_metas:
                print("doc_meta:", doc_meta)
        """

        if self._code != DashVectorCode.Success:
            return DashVectorResponse(None,
                                   exception=DashVectorException(code=DashVectorCode.RuntimeError,
                                                              reason="DashVectorSDK Collection initialize Failed",
                                                              request_id=self.request_id))

        try:
            query_request = QueryDocRequest(collection_meta=self._collection_meta,
                                            vector=vector,
                                            topk=topk,
                                            filter=filter,
                                            include_vector=include_vector,
                                            partition=partition,
                                            output_fields=output_fields)
        except DashVectorException as e:
            return DashVectorResponse(None, exception=e)

        return DashVectorResponse(self._handler.collection_query_doc(query_request, async_req=async_req))


    def delete(self,
               ids: Union[Union[str, int], List[Union[str, int]]],
               *,
               partition: Optional[str] = None,
               async_req: bool = False) -> DashVectorResponse:

        """
        Delete one or more Docs with ids(Primary Keys).

        Args:
           ids (Union[Union[str, int], List[Union[str, int]]]): one or more docs primary keys.
           partition (str): a partition name in collection. [optional]
           async_req (bool): use asynchronous operation, default is False.

        Return:
           DashVectorResponse, include code / message / request_id and a get() method,
                            code == DashVectorCode.Success means delete doc success, otherwise means failure.
                            if you use async_req, must call get() method first.

        Examples:
            [delete a doc]
            rsp = collection.delete(ids="primary_key")
            if not rsp:
                raise RuntimeError(f"Delete Failed, error:{rsp.code}, message:{rsp.message}")

            [delete multiple docs]
            rsp = collection.delete(ids=["primary_key_1", "primary_key_2", "primary_key_3"])
            if not rsp:
                raise RuntimeError(f"Delete Failed, error:{rsp.code}, message:{rsp.message}")

            [asynchronous delete a doc]
            rsp = collection.delete(ids="primary_key", async_req=True)
            if rsp.get().code != DashVectorCode.Success:
                raise RuntimeError(f"Delete Failed, error:{rsp.code}, message:{rsp.message}")
        """

        if self._code != DashVectorCode.Success:
            return DashVectorResponse(None,
                                   exception=DashVectorException(code=DashVectorCode.RuntimeError,
                                                              reason="DashVectorSDK Collection initialize Failed",
                                                              request_id=self.request_id))

        try:
            delete_request = DeleteDocRequest(collection_meta=self._collection_meta,
                                              ids=ids,
                                              partition=partition)
        except DashVectorException as e:
            return DashVectorResponse(None, exception=e)

        return DashVectorResponse(self._handler.collection_delete_doc(delete_request, async_req=async_req))

    def create_partition(self, name: str) -> DashVectorResponse:

        """
        Create a Partition in current Collection.

        Args:
           name (str): partition name

        Return:
           DashVectorResponse, include code / message / request_id,
                            code == DashVectorCode.Success means create partition success, otherwise means failure.

        Example:
            rsp = collection.create_partition("partition_name")
            if not rsp:
                raise RuntimeError(f"CreatePartition Failed, error:{rsp.code}, message:{rsp.message}")
        """

        if self._code != DashVectorCode.Success:
            return DashVectorResponse(None,
                                   exception=DashVectorException(code=DashVectorCode.RuntimeError,
                                                              reason="DashVectorSDK Collection initialize Failed",
                                                              request_id=self.request_id))

        try:
            create_request = CreatePartitionRequest(collection_meta=self._collection_meta,
                                                    partition_name=name)
        except DashVectorException as e:
            return DashVectorResponse(None, exception=e)

        return DashVectorResponse(self._handler.collection_create_partition(create_request, async_req=False))

    def delete_partition(self, name: str) -> DashVectorResponse:

        """
        Delete a Partition in current Collection.

        Args:
           name (str): partition name.

        Return:
           DashVectorResponse, include code / message / request_id,
                            code == DashVectorCode.Success means delete partition success, otherwise means failure.

        Example:
            rsp = collection.delete_partition("partition_name")
            if not rsp:
                raise RuntimeError(f"DeletePartition Failed, error:{rsp.code}, message:{rsp.message}")
        """

        if self._code != DashVectorCode.Success:
            return DashVectorResponse(None,
                                   exception=DashVectorException(code=DashVectorCode.RuntimeError,
                                                              reason="DashVectorSDK Collection initialize Failed",
                                                              request_id=self.request_id))

        try:
            drop_request = DropPartitionRequest(collection_meta=self._collection_meta,
                                                partition_name=name)
        except DashVectorException as e:
            return DashVectorResponse(None, exception=e)

        return DashVectorResponse(self._handler.collection_drop_partition(drop_request, async_req=False))

    def describe_partition(self, name: str) -> DashVectorResponse:

        """
        Describe a Partition Meta in current Collection.

        Args:
           name (str): partition name.

        Return:
           DashVectorResponse, include code / message / request_id / output,
                            code == DashVectorCode.Success means output is a partition meta.

        Example:
            rsp = collection.describe_partition("partition_name")
            if not rsp:
                raise RuntimeError(f"DescribePartition Failed, error:{rsp.code}, message:{rsp.message}")
            partition_meta = rsp.output
            print("partition_meta:", partition_meta)
        """

        if self._code != DashVectorCode.Success:
            return DashVectorResponse(None,
                                   exception=DashVectorException(code=DashVectorCode.RuntimeError,
                                                              reason="DashVectorSDK Collection initialize Failed",
                                                              request_id=self.request_id))

        try:
            describe_request = DescribeCollectionRequest(name=self._collection_meta.name)
        except DashVectorException as e:
            return DashVectorResponse(None, exception=e)

        describe_response = DashVectorResponse(self._handler.describe_collection(describe_request))
        if describe_response.code != DashVectorCode.Success:
            return describe_response

        try:
            collection_meta = CollectionMeta(meta=describe_response.output)
            partitions_meta = collection_meta.partitions
            if not isinstance(partitions_meta, dict):
                return DashVectorResponse(None,
                                       exception=DashVectorException(code=DashVectorCode.Internal,
                                                                  reason="DashVectorSDK Collection Partitions Meta Error"))
            if name not in partitions_meta:
                return DashVectorResponse(None,
                                       exception=DashVectorException(code=DashVectorCode.NotFound,
                                                                  reason="DashVectorSDK Collection Partition NotFound"))
            describe_response.output = partitions_meta[name]
            return describe_response
        except DashVectorException as e:
            return DashVectorResponse(None, exception=e)

    def has_partition(self, name: str) -> DashVectorResponse:

        """
        Determine a Partition exists in current Collection.

        Return:
           DashVectorResponse, include code / message / request_id / output,
                            code == DashVectorCode.Success means output is a partition determine status.

        Example:
            rsp = collection.has_partition("partition_name")
            if not rsp:
                raise RuntimeError(f"HasPartition Failed, error:{rsp.code}, message:{rsp.message}")
            has_partition = rsp.output
            print("has_partition:", has_partition)
        """

        if self._code != DashVectorCode.Success:
            return DashVectorResponse(None,
                                   exception=DashVectorException(code=DashVectorCode.RuntimeError,
                                                              reason="DashVectorSDK Collection initialize Failed",
                                                              request_id=self.request_id))

        describe_response = self.describe_partition(name)
        describe_response.output = True if describe_response.code == DashVectorCode.Success else False
        return describe_response

    def stats(self) -> DashVectorResponse:

        """
        Get Stats Info of current Collection.

        Return:
           DashVectorResponse, include code / message / request_id / output,
                            code == DashVectorCode.Success means output is a collection stats info dict.

        Example:
            rsp = collection.stats()
            if not rsp:
                raise RuntimeError(f"StatsCollection Failed, error:{rsp.code}, message:{rsp.message}")
            collection_stats = rsp.output
            print("collection_stats:", collection_stats)
        """

        if self._code != DashVectorCode.Success:
            return DashVectorResponse(None,
                                   exception=DashVectorException(code=DashVectorCode.RuntimeError,
                                                              reason="DashVectorSDK Collection initialize Failed",
                                                              request_id=self.request_id))

        try:
            stats_request = StatsCollectionRequest(name=self._collection_meta.name)
        except DashVectorException as e:
            return DashVectorResponse(None, exception=e)

        stats_response = DashVectorResponse(self._handler.stats_collection(stats_request))
        if stats_response.code != DashVectorCode.Success:
            return stats_response

        try:
            stats_response.output = CollectionStats(stats=stats_response.output)
            return stats_response
        except DashVectorException as e:
            return DashVectorResponse(None, exception=e)

    def stats_partition(self, name: str) -> DashVectorResponse:

        """
        Get Stats Info of a Partition in current Collection.

        Args:
           name (str): partition name

        Return:
           DashVectorResponse, include code / message / request_id / output,
                            code == DashVectorCode.Success means output is a partition stats info.

        Example:
            rsp = collection.stats_partition("partition_name")
            if not rsp:
                raise RuntimeError(f"StatsPartition Failed, error:{rsp.code}, message:{rsp.message}")
            partition_stats = rsp.output
            print("partition_stats:", partition_stats)
        """

        if self._code != DashVectorCode.Success:
            return DashVectorResponse(None,
                                   exception=DashVectorException(code=DashVectorCode.RuntimeError,
                                                              reason="DashVectorSDK Collection initialize Failed",
                                                              request_id=self.request_id))

        stats_response = self.stats()
        if stats_response.code != DashVectorCode.Success:
            return stats_response

        if not isinstance(stats_response.output, CollectionStats):
            return DashVectorResponse(None,
                                   exception=DashVectorException(code=DashVectorCode.Internal,
                                                              reason="DashVectorSDK Collection Partitions Stats Error",
                                                              request_id=stats_response.request_id))

        partitions_stats = stats_response.output.partitions
        if not isinstance(partitions_stats, dict):
            return DashVectorResponse(None,
                                   exception=DashVectorException(code=DashVectorCode.Internal,
                                                              reason="DashVectorSDK Collection Partitions Stats Error",
                                                              request_id=stats_response.request_id))
        if name not in partitions_stats:
            return DashVectorResponse(None,
                                   exception=DashVectorException(code=DashVectorCode.NotFound,
                                                              reason="DashVectorSDK Collection Partition NotFound",
                                                              request_id=stats_response.request_id))
        stats_response.output = partitions_stats[name]
        return stats_response

    def list_partitions(self) -> DashVectorResponse:

        """
        List all Partition Names in current Collection.

        Return:
           DashVectorResponse, include code / message / request_id / output,
                            code == DashVectorCode.Success means output is a partition name list.

        Example:
            rsp = collection.list_partitions()
            if not rsp:
                raise RuntimeError(f"ListPartition Failed, error:{rsp.code}, message:{rsp.message}")
            partition_list = rsp.output
            print("partition_list:", partition_list)
        """

        if self._code != DashVectorCode.Success:
            return DashVectorResponse(None,
                                   exception=DashVectorException(code=DashVectorCode.RuntimeError,
                                                              reason="DashVectorSDK Collection initialize Failed",
                                                              request_id=self.request_id))

        try:
            describe_request = DescribeCollectionRequest(name=self._collection_meta.name)
        except DashVectorException as e:
            return DashVectorResponse(None, exception=e)

        describe_response = DashVectorResponse(self._handler.describe_collection(describe_request))
        if describe_response.code != DashVectorCode.Success:
            return describe_response

        try:
            collection_meta = CollectionMeta(meta=describe_response.output)
            partitions_meta = collection_meta.partitions
            partition_list = []
            for partition_name, partition_meta in partitions_meta.items():
                partition_list.append(partition_name)
            describe_response.output = partition_list
            return describe_response
        except DashVectorException as e:
            return DashVectorResponse(None, exception=e)

    def __init__(self,
                 response: Optional[RPCResponse] = None,
                 collection_meta: Optional[CollectionMeta] = None,
                 handler: Optional[RPCHandler] = None,
                 exception: Optional[DashVectorException] = None):
        """
        a DashVector Collection Instance which create by DashVector.client.get("collection_name")

        Returns:
            Collection, includes a series of Doc related operations
        """

        super().__init__(response, exception=exception)
        self._collection_meta = collection_meta
        self._handler = handler

        self.get()

    def __str__(self):
        if self._collection_meta is not None:
            return self._collection_meta.__str__()
        return super().__str__()

    def __repr__(self):
        if self._collection_meta is not None:
            return self._collection_meta.__repr__()
        return super().__repr__()

    def __bool__(self):
        return self._code == DashVectorCode.Success
