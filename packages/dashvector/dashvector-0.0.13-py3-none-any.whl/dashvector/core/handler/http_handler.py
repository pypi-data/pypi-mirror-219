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
import _thread
import asyncio
import aiohttp

from typing import Dict, Optional

from dashvector.common.error import DashVectorCode, DashVectorException, DashVectorHTTPException
from dashvector.common.status import PartitionStatus
from dashvector.common.handler import RPCResponse, RPCHandler

from dashvector.core.models.create_collection_request import CreateCollectionRequest
from dashvector.core.models.describe_collection_request import DescribeCollectionRequest
from dashvector.core.models.stats_collection_request import StatsCollectionRequest
from dashvector.core.models.drop_collection_request import DropCollectionRequest
from dashvector.core.models.upsert_doc_request import UpsertDocRequest
from dashvector.core.models.delete_doc_request import DeleteDocRequest
from dashvector.core.models.get_doc_request import GetDocRequest
from dashvector.core.models.query_doc_request import QueryDocRequest
from dashvector.core.models.create_partition_request import CreatePartitionRequest
from dashvector.core.models.drop_partition_request import DropPartitionRequest
from dashvector.core.doc import DocBuilder

from dashvector.version import __version__


class HTTPHandler(RPCHandler):
    _COLLECTION_MANAGE_URL = "/v1/collection/"
    _COLLECTION_STATS_URL = "/v1/collection/%s/stats"
    _COLLECTION_LIST_URL = "/v1/collections"
    _DOC_WRITE_URL = "/v1/collection/%s/doc"
    _DOC_QUERY_URL = "/v1/collection/%s/query"
    _DOC_QUERY_BY_SQL_URL = "/v1/collection/sql"
    _DOC_GET_BY_KEY_URL = "/v1/collection/%s/doc?key=%s"
    _PARTITION_CREATE_URL = "/v1/collection/partition"
    _PARTITION_MANAGE_URL = "/v1/collection/%s/%s"
    _VERSION_URL = "/service_version"

    class _HTTPResponse(RPCResponse):
        def __init__(self,
                     future,
                     *,
                     req=None,
                     async_req=False,
                     attr_name=None):

            super().__init__(async_req=async_req)
            self._future = future
            self._attr_name = attr_name
            self._status = None
            self._headers = None
            self._body = None
            self._request = None
            self._response = None

        def get(self):
            if self._response is None:
                feature_result = self._future.result(timeout=3600)

                self._status = feature_result['status'] if 'status' in feature_result else -1
                self._headers = feature_result['headers'] if 'headers' in feature_result else {}
                if self._status != 200:
                    raise DashVectorHTTPException(code=self._status,
                                               request_id=self.get_request_id())
                self._body = feature_result['body'] if 'body' in feature_result else ""
                self._response = self._parse_response(self._body,
                                                      attr_name=self._attr_name)

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
            return None

        def get_request_id(self):
            self._request_id = ""
            if isinstance(self._headers, dict) and 'request_id' in self._headers:
                self._request_id = self._headers['request_id']
            return self._request_id

        @property
        def request_id(self):
            return self.get_request_id()

        def _parse_response(self, text, attr_name=None):
            try:
                text_json = {} if text is None else json.loads(text)
            except Exception as e:
                raise DashVectorException(code=DashVectorCode.Internal,
                                       reason=f"DashVector Response Parse Failed, Text:{text}")

            if 'status' not in text_json \
                    or 'code' not in text_json['status'] \
                    or 'reason' not in text_json['status']:
                raise DashVectorException(code=DashVectorCode.Internal,
                                       reason=f"DashVector Response Parse Failed, Text:{text}")
            if text_json['status']['code'] != DashVectorCode.Success:
                if text_json['status']['code'] == DashVectorCode.NotFound and attr_name == 'has_partition':
                    return False
                raise DashVectorException(code=text_json['status']['code'],
                                       reason=text_json['status']['reason'])

            if attr_name is None:
                return None
            if attr_name == "doc":
                return text_json["docs"] if 'docs' in text_json else []
            if attr_name == 'has_partition':
                return True if 'partition_status' in text_json else False
            if attr_name == 'list_partition':
                return text_json['collection']['partitions'] if 'collection' in text_json and 'partitions' in text_json['collection'] else {}
            if attr_name not in text_json:
                return None
            return text_json[attr_name]

    class _HTTPAsyncClient(object):
        _aio_ev_loop = None

        @staticmethod
        def _start_aio_ev_thread(loop):
            loop.run_forever()

        def __init__(self,
                     *,
                     endpoint: str,
                     headers: Optional[Dict] = None,
                     timeout: float = 10.0):
            self._endpoint = endpoint
            self._headers = {} if headers is None else headers
            self._timeout = timeout

            if HTTPHandler._HTTPAsyncClient._aio_ev_loop is None:
                HTTPHandler._HTTPAsyncClient._aio_ev_loop = asyncio.get_event_loop()
                _thread.start_new_thread(HTTPHandler._HTTPAsyncClient._start_aio_ev_thread,
                                         (HTTPHandler._HTTPAsyncClient._aio_ev_loop,))
                while not HTTPHandler._HTTPAsyncClient._aio_ev_loop.is_running():
                    pass

        def _request(self, url, headers, timeout):
            url = "http://" + self._endpoint + url
            if headers is None:
                headers = self._headers
            if timeout is None:
                timeout = self._timeout
            return url, headers, timeout

        async def _response(self, rsp):
            await rsp.read()
            rsp_status = rsp.status
            rsp_headers = {}
            for header_k, header_v in rsp.headers.items():
                rsp_headers[header_k] = header_v
            rsp_body = await rsp.text() if rsp_status == 200 else ""

            return {
                "status": rsp_status,
                "headers": rsp_headers,
                "body": rsp_body
            }

        async def _get(self, url, headers=None, timeout=None):
            url, headers, timeout = self._request(url, headers, timeout)
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=timeout) as rsp:
                    return await self._response(rsp)

        async def _post(self, url, data, headers=None, timeout=None):
            url, headers, timeout = self._request(url, headers, timeout)
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=data, headers=headers, timeout=timeout) as rsp:
                    return await self._response(rsp)

        async def _put(self, url, data, headers=None, timeout=None):
            url, headers, timeout = self._request(url, headers, timeout)
            async with aiohttp.ClientSession() as session:
                async with session.put(url, data=data, headers=headers, timeout=timeout) as rsp:
                    return await self._response(rsp)

        async def _delete(self, url, data=None, headers=None, timeout=None):
            url, headers, timeout = self._request(url, headers, timeout)
            async with aiohttp.ClientSession() as session:
                async with session.delete(url, data=data, headers=headers, timeout=timeout) as rsp:
                    return await self._response(rsp)

        def get(self,
                url,
                *,
                headers=None,
                timeout=None,
                req=None,
                async_req=False,
                attr_name=None):
            a_future = asyncio.run_coroutine_threadsafe(self._get(url, headers, timeout),
                                                        loop=HTTPHandler._HTTPAsyncClient._aio_ev_loop)
            return HTTPHandler._HTTPResponse(a_future,
                                             req=req,
                                             async_req=async_req,
                                             attr_name=attr_name)

        def post(self,
                 url,
                 data,
                 *,
                 headers=None,
                 timeout=None,
                 req=None,
                 async_req=False,
                 attr_name=None):
            a_future = asyncio.run_coroutine_threadsafe(self._post(url, data, headers, timeout),
                                                        loop=HTTPHandler._HTTPAsyncClient._aio_ev_loop)
            return HTTPHandler._HTTPResponse(a_future,
                                             req=req,
                                             async_req=async_req,
                                             attr_name=attr_name)

        def put(self,
                url,
                data,
                *,
                headers=None,
                timeout=None,
                req=None,
                async_req=False,
                attr_name=None):
            a_future = asyncio.run_coroutine_threadsafe(self._put(url, data, headers, timeout),
                                                        loop=HTTPHandler._HTTPAsyncClient._aio_ev_loop)
            return HTTPHandler._HTTPResponse(a_future,
                                             req=req,
                                             async_req=async_req,
                                             attr_name=attr_name)

        def delete(self,
                   url,
                   data=None,
                   *,
                   headers=None,
                   timeout=None,
                   req=None,
                   async_req=False,
                   attr_name=None):
            a_future = asyncio.run_coroutine_threadsafe(self._delete(url, data, headers, timeout),
                                                        loop=HTTPHandler._HTTPAsyncClient._aio_ev_loop)
            return HTTPHandler._HTTPResponse(a_future,
                                             req=req,
                                             async_req=async_req,
                                             attr_name=attr_name,)

    def __init__(self, *,
                 endpoint: str,
                 api_key: str = "",
                 timeout: float = 10.0):

        """
        endpoint: str
        """
        if not isinstance(endpoint, str):
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK HTTPHandler endpoint Type({endpoint}) is Invalid")

        if len(endpoint) <= 0:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK HTTPHandler endpoint Empty")

        """
        api_key: str
        """
        if not isinstance(api_key, str):
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK HTTPHandler api_key Type({api_key}) is Invalid")

        """
        timeout: float
        """
        if isinstance(timeout, float):
            pass
        elif isinstance(timeout, int):
            timeout = float(timeout)
        else:
            raise DashVectorException(code=DashVectorCode.InvalidArgument,
                                   reason=f"DashVectorSDK HTTPHandler timeout Type({timeout}) is Invalid")
        if timeout <= 0.000001:
            timeout = 365.5 * 86400

        super().__init__(endpoint=endpoint,
                         api_key=api_key,
                         timeout=timeout)
        self._http_headers = {'dashvector-auth-token': self._api_key,
                              'dashvector-version': __version__}
        self._http_async_client = self._HTTPAsyncClient(endpoint=self._endpoint,
                                                        headers=self._http_headers,
                                                        timeout=self._timeout)

    def create_collection(self,
                          create_request: CreateCollectionRequest,
                          *,
                          async_req: bool = False) -> RPCResponse:
        rebuild_timeout = self._timeout
        if rebuild_timeout < 30.0:
            rebuild_timeout = 30.0
        return self._http_async_client.post(self._COLLECTION_MANAGE_URL, create_request.to_json(),
                                            timeout=rebuild_timeout,
                                            async_req=async_req)

    def drop_collection(self,
                        drop_request: DropCollectionRequest,
                        *,
                        async_req: bool = False) -> RPCResponse:
        rebuild_timeout = self._timeout
        if rebuild_timeout < 30.0:
            rebuild_timeout = 30.0
        return self._http_async_client.delete(self._COLLECTION_MANAGE_URL + drop_request.name,
                                              timeout=rebuild_timeout,
                                              async_req=async_req)

    def describe_collection(self,
                            describe_request: DescribeCollectionRequest,
                            *,
                            async_req: bool = False) -> RPCResponse:
        return self._http_async_client.get(self._COLLECTION_MANAGE_URL + describe_request.name, attr_name="collection",
                                           async_req=async_req)

    def stats_collection(self,
                         stats_request: StatsCollectionRequest,
                         *,
                         async_req: bool = False) -> RPCResponse:
        return self._http_async_client.get(self._COLLECTION_STATS_URL % stats_request.name, attr_name="collection_stats",
                                           async_req=async_req)

    def list_collections(self,
                         *,
                         async_req: bool = False) -> RPCResponse:
        return self._http_async_client.get(self._COLLECTION_LIST_URL, async_req=async_req, attr_name="collections")

    def get_version(self,
                    *,
                    async_req: bool = False):
        return self._http_async_client.get(self._VERSION_URL, async_req=async_req, attr_name="version")

    def collection_insert_doc(self,
                              insert_request: UpsertDocRequest,
                              *,
                              async_req: bool = False) -> RPCResponse:
        return self._http_async_client.post(self._DOC_WRITE_URL % insert_request.collection_name, insert_request.to_json(),
                                            async_req=async_req)

    def collection_update_doc(self,
                              update_request: UpsertDocRequest,
                              *,
                              async_req: bool = False) -> RPCResponse:
        return self._http_async_client.put(self._DOC_WRITE_URL % update_request.collection_name, update_request.to_json(),
                                           async_req=async_req)

    def collection_delete_doc(self,
                              delete_request: DeleteDocRequest,
                              *,
                              async_req: bool = False) -> RPCResponse:
        return self._http_async_client.delete(self._DOC_WRITE_URL % delete_request.collection_name, delete_request.to_json(),
                                              async_req=async_req)

    def collection_get_doc_by_key(self,
                                  get_request: GetDocRequest,
                                  *,
                                  async_req: bool = False) -> RPCResponse:
        return self._http_async_client.get(self._DOC_GET_BY_KEY_URL % (get_request.collection_name, get_request.primary_key),
                                           attr_name="docs",
                                           async_req=async_req)

    def collection_query_doc(self,
                             query_request: QueryDocRequest,
                             *,
                             async_req: bool = False) -> RPCResponse:
        return self._http_async_client.post(self._DOC_QUERY_URL % query_request.collection_name, query_request.to_json(),
                                            req=query_request,
                                            attr_name="doc_results",
                                            async_req=async_req)

    def collection_create_partition(self,
                                    create_request: CreatePartitionRequest,
                                    *,
                                    async_req: bool = False) -> RPCResponse:
        return self._http_async_client.post(self._PARTITION_CREATE_URL, create_request.to_json(),
                                            async_req=async_req)

    def collection_drop_partition(self,
                                  drop_request: DropPartitionRequest,
                                  *,
                                  async_req: bool = False) -> RPCResponse:
        return self._http_async_client.delete(self._PARTITION_MANAGE_URL % (drop_request.collection_name, drop_request.partition_name),
                                              async_req=async_req)

    def close(self) -> None:
        return None
