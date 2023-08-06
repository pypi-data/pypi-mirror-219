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

from enum import IntEnum
import grpc
import http


class DashVectorCode(IntEnum):
    InvalidArgument = -49999
    NotFound = -49998
    AlreadyExist = -49997
    FailedPrecondition = -49996
    Unauthorized = -49995
    Internal = -49994
    Streamer = -49993
    Searcher = -49992
    Frontend = -49991
    Indexer = -49990
    RuntimeError = -1000
    LogicError = -1001
    StatusError = -1002
    LoadConfig = -1003
    ConfigError = -1004
    NotInitialized = -1006
    OpenFile = -1007
    ReadData = -1008
    WriteData = -1009
    ExceedLimit = -1010
    SerializeError = -1011
    DeserializeError = -1012
    StartServer = -1013
    StoppedService = -1014
    FileSystem = -1015
    RpcError = -1016
    InitChannelError = -1017
    AddSubChannelError = -1018
    NoNeedProcess = -1019
    EtcdError = -1020
    MessageQueueError = -1021
    KafkaSubTopicExistErr = -1022
    KafkaUnSubTopicNotExistErr = -1023
    InitKafkaError = -1024
    KafkaPublishError = -1025
    EmptyCollectionName = -2000
    EmptyColumnName = -2001
    EmptyColumns = -2002
    EmptyRepositoryTable = -2003
    EmptyRepositoryName = -2004
    EmptyUserName = -2005
    EmptyPassword = -2006
    InvalidURI = -2007
    InvalidCollectionStatus = -2008
    InvalidRecord = -2009
    InvalidQuery = -2010
    InvalidIndexDataFormat = -2011
    InvalidWriteRequest = -2012
    InvalidVectorFormat = -2013
    InvalidRepositoryType = -2014
    InvalidDataType = -2015
    InvalidIndexType = -2016
    InvalidSegment = -2017
    InvalidRevision = -2018
    InvalidFeature = -2019
    MismatchedSchema = -2020
    MismatchedMagicNumber = -2021
    MismatchedIndexColumn = -2022
    MismatchedDimension = -2023
    MismatchedDataType = -2024
    EmptyTopicName = -2025
    EmptyAliasName = -2026
    EmptyAliasCollectionName = -2027
    OutOfChannelRange = -2028
    InexistentSegment = -2029
    UpdateStatusField = -3000
    UpdateRevisionField = -3001
    UpdateCollectionUIDField = -3002
    UpdateIndexTypeField = -3003
    UpdateDataTypeField = -3004
    UpdateParametersField = -3005
    UpdateRepositoryTypeField = -3006
    UpdateColumnNameField = -3007
    ZeroDocsPerSegment = -3008
    UnsupportedConnection = -3009
    DuplicateAlias = -3010
    InvalidAlias = -3011
    InexistentAlias = -3012
    DuplicateCollection = -4000
    DuplicateKey = -4001
    InexistentCollection = -4002
    InexistentColumn = -4003
    InexistentKey = -4004
    SuspendedCollection = -4005
    LostSegment = -4006
    EmptyLsnContext = -4007
    ExceedRateLimit = -4008
    WalWriteFailure = -4009
    RaftError = -4010
    WritingDisabled = -4011
    WalRecoverFailure = -4012
    InvalidKey = -4013
    UnavailableSegment = -5000
    MismatchedForward = -5001
    OutOfBoundsResult = -5002
    UnreadyQueue = -5003
    ScheduleError = -5004
    UnreadableCollection = -5005
    TaskIsRunning = -5006
    UnsupportedCondition = -5007
    UnsupportedFunction = -5008
    UnacceptedCondition = -5009
    OrderbyNotInSelectItems = -5010
    PbToSqlInfoError = -5011
    MismatchedQueryType = -5012
    ExistentSegment = -5013
    DownLoadFromOssFailure = -5014
    SubscribeMqFailure = -5015
    UnSubscribeMqFailure = -5016
    DownloadFile = -6000
    EmptyPrimaryKey = -30000
    EmptyDocList = -30001
    EmptyDocFields = -30002
    InvalidField = -30003
    DuplicateField = -30004
    EmptyIndexField = -30005
    DuplicateServer = -30006
    InexistentServer = -30007
    InexistentCollectionServerGroup = -30008
    DuplicateCollectionServerGroup = -30009
    IgnoreEtcdPath = -30010
    EmptyLoadBalancer = -30011
    MismatchedBatchResult = -30012
    IgnoreCollectionStatus = -30013
    IgnoreSegmentStatus = -30014
    IgnoreSegmentMeta = -30015
    Unknown = -999
    Closed = -998
    Timeout = 408
    Success = 0


class DashVectorCodeMap(object):
    _map_rules = {
        DashVectorCode.EmptyCollectionName: DashVectorCode.InvalidArgument,
        DashVectorCode.EmptyColumnName: DashVectorCode.InvalidArgument,
        DashVectorCode.EmptyColumns : DashVectorCode.InvalidArgument,
        DashVectorCode.EmptyRepositoryTable: DashVectorCode.InvalidArgument,
        DashVectorCode.EmptyRepositoryName: DashVectorCode.InvalidArgument,
        DashVectorCode.EmptyUserName: DashVectorCode.InvalidArgument,
        DashVectorCode.EmptyPassword: DashVectorCode.InvalidArgument,
        DashVectorCode.InvalidURI: DashVectorCode.InvalidArgument,
        DashVectorCode.InvalidCollectionStatus: DashVectorCode.InvalidArgument,
        DashVectorCode.InvalidRecord: DashVectorCode.InvalidArgument,
        DashVectorCode.InvalidQuery: DashVectorCode.InvalidArgument,
        DashVectorCode.InvalidIndexDataFormat: DashVectorCode.InvalidArgument,
        DashVectorCode.InvalidWriteRequest: DashVectorCode.InvalidArgument,
        DashVectorCode.InvalidVectorFormat: DashVectorCode.InvalidArgument,
        DashVectorCode.InvalidRepositoryType: DashVectorCode.InvalidArgument,
        DashVectorCode.InvalidDataType: DashVectorCode.InvalidArgument,
        DashVectorCode.InvalidIndexType: DashVectorCode.InvalidArgument,
        DashVectorCode.InvalidSegment: DashVectorCode.InvalidArgument,
        DashVectorCode.InvalidRevision: DashVectorCode.InvalidArgument,
        DashVectorCode.InvalidFeature: DashVectorCode.InvalidArgument,
        DashVectorCode.MismatchedSchema: DashVectorCode.InvalidArgument,
        DashVectorCode.EmptyPrimaryKey: DashVectorCode.InvalidArgument,
        DashVectorCode.EmptyDocList: DashVectorCode.InvalidArgument,
        DashVectorCode.InvalidField: DashVectorCode.InvalidArgument,
        DashVectorCode.DuplicateField: DashVectorCode.InvalidArgument,
        DashVectorCode.EmptyIndexField: DashVectorCode.InvalidArgument,
        DashVectorCode.UnsupportedConnection: DashVectorCode.InvalidArgument
    }

    @staticmethod
    def rewrite(code: DashVectorCode):
        if code not in DashVectorCodeMap._map_rules:
            return code
        return DashVectorCodeMap._map_rules[code]


class DashVectorException(Exception):
    """
    DashVector Exception
    """

    def __init__(self, code=DashVectorCode.InvalidArgument, reason=None, request_id=None):
        self._code = DashVectorCodeMap.rewrite(code)
        self._reason = "Invalid Argument" if reason is None else reason
        self._request_id = request_id
        super().__init__(f'{self._reason}({self._code})')

    @property
    def code(self):
        return self._code

    @property
    def message(self):
        return self._reason

    @property
    def request_id(self):
        if self._request_id is None:
            return ""
        return self._request_id


class DashVectorHTTPException(DashVectorException):
    def __new__(cls, code, reason=None, request_id=None):
        if code == http.HTTPStatus.UNAUTHORIZED:
            reason = "DashVectorSDK RPC No Permission" if reason is None else reason
            return DashVectorException(code=DashVectorCode.Unauthorized, reason=reason, request_id=request_id)
        if code == http.HTTPStatus.FORBIDDEN:
            reason = "DashVectorSDK RPC Request Forbidden" if reason is None else reason
            return DashVectorException(code=DashVectorCode.Unauthorized, reason=reason, request_id=request_id)
        if code == http.HTTPStatus.SERVICE_UNAVAILABLE:
            reason = "DashVectorSDK RPC Server ExceedRateLimit" if reason is None else reason
            return DashVectorException(code=DashVectorCode.ExceedRateLimit, reason=reason, request_id=request_id)
        if code == http.HTTPStatus.INTERNAL_SERVER_ERROR:
            reason = "DashVectorSDK RPC Internal Server Error" if reason is None else reason
            return DashVectorException(code=DashVectorCode.Internal, reason=reason, request_id=request_id)
        if code == http.HTTPStatus.GATEWAY_TIMEOUT:
            reason = "DashVectorSDK RPC Request Timeout" if reason is None else reason
            return DashVectorException(code=DashVectorCode.Timeout, reason=reason, request_id=request_id)
        reason = "DashVectorSDK RPC Internal Server Error" if reason is None else reason
        return DashVectorException(code=DashVectorCode.Internal, reason=reason, request_id=request_id)


class DashVectorGRPCException(DashVectorException):
    def __new__(cls, code, reason=None, request_id=None):
        if code == grpc.StatusCode.PERMISSION_DENIED:
            reason = "DashVectorSDK RPC No Permission" if reason is None or len(reason) == 0 else reason
            return DashVectorException(code=DashVectorCode.Unauthorized, reason=reason, request_id=request_id)
        if code == grpc.StatusCode.UNAUTHENTICATED:
            reason = "DashVectorSDK RPC Request Forbidden" if reason is None or len(reason) == 0 else reason
            return DashVectorException(code=DashVectorCode.Unauthorized, reason=reason, request_id=request_id)
        if code == grpc.StatusCode.DEADLINE_EXCEEDED:
            reason = "DashVectorSDK RPC Request Timeout" if reason is None or len(reason) == 0 else reason
            return DashVectorException(code=DashVectorCode.Timeout, reason=reason, request_id=request_id)
        if code == grpc.StatusCode.ABORTED:
            reason = "DashVectorSDK RPC Server ExceedRateLimit" if reason is None or len(reason) == 0 else reason
            return DashVectorException(code=DashVectorCode.ExceedRateLimit, reason=reason, request_id=request_id)
        if code == grpc.StatusCode.INTERNAL:
            reason = "DashVectorSDK RPC Internal Server Error" if reason is None or len(reason) == 0 else reason
            return DashVectorException(code=DashVectorCode.Internal, reason=reason, request_id=request_id)
        reason = "DashVectorSDK RPC Internal Server Error" if reason is None or len(reason) == 0 else reason
        return DashVectorException(code=DashVectorCode.Internal, reason=reason, request_id=request_id)
