#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2020 FABRIC Testbed
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
# Author: Komal Thareja (kthare10@renci.org)
import enum
import json
import traceback
from datetime import datetime
from typing import Tuple, Any, List, Union

from atomicwrites import atomic_write

from fabric_cm.credmgr import swagger_client
from fabric_cm.credmgr.swagger_client import Token
from fabric_cm.credmgr.swagger_client.rest import ApiException as CredMgrException


@enum.unique
class Status(enum.Enum):
    OK = 1
    INVALID_ARGUMENTS = 2
    FAILURE = 3

    def interpret(self, exception=None):
        interpretations = {
            1: "Success",
            2: "Invalid Arguments",
            3: "Failure"
          }
        if exception is None:
            return interpretations[self.value]
        else:
            return str(exception) + ". " + interpretations[self.value]


class TokenState(enum.Enum):
    Nascent = enum.auto(),
    Valid = enum.auto(),
    Refreshed = enum.auto(),
    Revoked = enum.auto(),
    Expired = enum.auto(),

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @staticmethod
    def state_from_str(state: str):
        if state is None:
            return state

        for t in TokenState:
            if state == str(t):
                return t

        return None

    @staticmethod
    def state_list_to_str_list(states: list):
        if states is None:
            result = []

            for t in TokenState:
                result.append(str(t))
            return result

        result = []
        for t in states:
            result.append(str(t))

        return result


class CredmgrProxy:
    """
    Credential Manager Proxy
    """
    ID_TOKEN = "id_token"
    REFRESH_TOKEN = "refresh_token"
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S %z"
    CREATED_AT = "created_at"
    ERROR = "error"
    PROP_AUTHORIZATION = 'Authorization'
    PROP_BEARER = 'Bearer'

    def __init__(self, credmgr_host: str):
        self.host = credmgr_host
        self.tokens_api = None
        if credmgr_host is not None:
            # create an instance of the API class
            configuration = swagger_client.configuration.Configuration()
            configuration.host = f"https://{credmgr_host}/credmgr/"
            api_instance = swagger_client.ApiClient(configuration)
            self.tokens_api = swagger_client.TokensApi(api_client=api_instance)
            self.default_api = swagger_client.DefaultApi(api_client=api_instance)
            self.version_api = swagger_client.VersionApi(api_client=api_instance)

    def __set_tokens(self, *, token: str):
        """
        Set tokens
        @param token token
        """
        # Set the tokens
        self.tokens_api.api_client.configuration.api_key[self.PROP_AUTHORIZATION] = token
        self.tokens_api.api_client.configuration.api_key_prefix[self.PROP_AUTHORIZATION] = self.PROP_BEARER

    def refresh(self, project_id: str, scope: str, refresh_token: str,
                file_name: str = None) -> Tuple[Status, dict]:
        """
        Refresh token
        @param project_id Project Id
        @param scope scope
        @param refresh_token refresh token
        @param file_name File name
        @returns Tuple of Status, dictionary {id_token/error, refresh_token, created_at}. In case of failure, id token would be None
        @raises Exception in case of failure
        """
        try:
            body = swagger_client.Request(refresh_token)
            tokens = self.tokens_api.tokens_refresh_post(body=body, project_id=project_id, scope=scope)

            tokens_json = tokens.data[0].to_dict()
            if file_name is not None:
                with atomic_write(file_name, overwrite=True) as f:
                    json.dump(tokens_json, f)
            return Status.OK, tokens_json
        except CredMgrException as e:
            message = str(e.body)
            tokens_json = {self.ERROR: e.body,
                           self.CREATED_AT: datetime.strftime(datetime.utcnow(), self.TIME_FORMAT)}
            if message is not None and self.REFRESH_TOKEN in message:
                refresh_token = message.split(f"{self.REFRESH_TOKEN}:")[1]
                refresh_token = refresh_token.strip()
                refresh_token = refresh_token.strip("\"")
                refresh_token = refresh_token.strip("\n")
                tokens_json[self.REFRESH_TOKEN] = refresh_token
            return Status.FAILURE, tokens_json

    def revoke(self, refresh_token: str) -> Tuple[Status, Any]:
        """
        Revoke token
        @param refresh_token refresh token
        @returns response
        @raises Exception in case of failure
        """
        try:
            body = swagger_client.Request(refresh_token)
            self.tokens_api.tokens_revoke_post(body=body)

            return Status.OK, None
        except CredMgrException as e:
            return Status.FAILURE, e.body

    def clear_token_cache(self, *, file_name: str) -> Tuple[Status, Any]:
        """
        Clear cached token
        @param file_name name of the file containing the cached token
        @return STATUS.OK for success, STATUS.FAILURE and exception in case of failure
        """
        try:
            with open(file_name, 'r') as stream:
                token_data = json.loads(stream.read())
            if self.ID_TOKEN in token_data:
                token_data.pop(self.ID_TOKEN)
            with atomic_write(file_name, overwrite=True) as f:
                json.dump(token_data, f)
        except Exception as e:
            return Status.FAILURE, e
        return Status.OK, None

    def certs_get(self) -> Tuple[Status, Any]:
        """
        Return certificates
        """
        try:
            certs = self.default_api.certs_get()
            return Status.OK, certs
        except CredMgrException as e:
            return Status.FAILURE, e.body

    def version_get(self) -> Tuple[Status, Any]:
        """
        Return Version
        """
        try:
            version = self.version_api.version_get()
            return Status.OK, version
        except CredMgrException as e:
            return Status.FAILURE, e.body

    def tokens(self, *, token: str, project_id: str = None, expires: str = None, states: List[TokenState] = None,
               limit: int = 200, offset: int = 0, token_hash: str = None,) -> Tuple[Status, Union[Exception, List[Token]]]:
        """
        Return list of tokens issued to a user
        @return list of tokens
        """
        if token is None:
            return Status.INVALID_ARGUMENTS, CredMgrException(f"Token {token} must be specified")

        try:
            # Set the tokens
            self.__set_tokens(token=token)

            if expires is not None:
                expiry_time = datetime.strptime(expires, self.TIME_FORMAT)
            else:
                expiry_time = None

            tokens = self.tokens_api.tokens_get(states=TokenState.state_list_to_str_list(states=states), limit=limit,
                                                offset=offset, token_hash=token_hash, project_id=project_id,
                                                expires=expiry_time)

            return Status.OK, tokens.data if tokens.data is not None else []
        except Exception as e:
            return Status.FAILURE, e

    def token_revoke_list(self, *, token: str, project_id: str) -> Tuple[Status, Union[Exception, List[str]]]:
        """
        Return list of revoked tokens for a user
        @return list of revoked tokens
        """
        if token is None or project_id is None:
            return Status.INVALID_ARGUMENTS, CredMgrException(f"Token {token} and "
                                                              f"Project Id {project_id} must be specified")

        try:
            # Set the tokens
            self.__set_tokens(token=token)

            slices = self.tokens_api.tokens_revoke_list_get(project_id=project_id)

            return Status.OK, slices.data if slices.data is not None else []
        except Exception as e:
            return Status.FAILURE, e