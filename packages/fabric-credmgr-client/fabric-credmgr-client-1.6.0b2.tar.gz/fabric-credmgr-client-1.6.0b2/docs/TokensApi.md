# swagger_client.TokensApi

All URIs are relative to *http://127.0.0.1:7000/credmgr/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**tokens_create_post**](TokensApi.md#tokens_create_post) | **POST** /tokens/create | Generate tokens for an user
[**tokens_get**](TokensApi.md#tokens_get) | **GET** /tokens | Get tokens
[**tokens_refresh_post**](TokensApi.md#tokens_refresh_post) | **POST** /tokens/refresh | Refresh tokens for an user
[**tokens_revoke_list_get**](TokensApi.md#tokens_revoke_list_get) | **GET** /tokens/revoke_list | Get token revoke list i.e. list of revoked identity token hashes
[**tokens_revoke_post**](TokensApi.md#tokens_revoke_post) | **POST** /tokens/revoke | Revoke a token for an user
[**tokens_revokes_post**](TokensApi.md#tokens_revokes_post) | **POST** /tokens/revokes | Revoke a token
[**tokens_validate_post**](TokensApi.md#tokens_validate_post) | **POST** /tokens/validate | Validate an identity token issued by Credential Manager

# **tokens_create_post**
> Tokens tokens_create_post(project_id=project_id, scope=scope, lifetime=lifetime, comment=comment)

Generate tokens for an user

Request to generate tokens for an user 

### Example
```python
from __future__ import print_function
import time
from fabric_cm.credmgr.swagger_client import TokensApi
from fabric_cm.credmgr.swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = TokensApi()
project_id = 'project_id_example' # str | Project identified by universally unique identifier (optional)
scope = 'all' # str | Scope for which token is requested (optional) (default to all)
lifetime = 4 # int | Lifetime of the token requested in hours (optional) (default to 4)
comment = 'Create Token via GUI' # str | Comment (optional) (default to Create Token via GUI)

try:
    # Generate tokens for an user
    api_response = api_instance.tokens_create_post(project_id=project_id, scope=scope, lifetime=lifetime, comment=comment)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TokensApi->tokens_create_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project identified by universally unique identifier | [optional] 
 **scope** | **str**| Scope for which token is requested | [optional] [default to all]
 **lifetime** | **int**| Lifetime of the token requested in hours | [optional] [default to 4]
 **comment** | **str**| Comment | [optional] [default to Create Token via GUI]

### Return type

[**Tokens**](Tokens.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tokens_get**
> Tokens tokens_get(token_hash=token_hash, project_id=project_id, expires=expires, states=states, limit=limit, offset=offset)

Get tokens

Get tokens for a user in a project 

### Example
```python
from __future__ import print_function
import time
from fabric_cm.credmgr.swagger_client import TokensApi
from fabric_cm.credmgr.swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = TokensApi()
token_hash = 'token_hash_example' # str | Token identified by SHA256 hash (optional)
project_id = 'project_id_example' # str | Project identified by universally unique identifier (optional)
expires = 'expires_example' # str | Search for tokens with expiry time lesser than the specified expiration time (optional)
states = ['states_example'] # list[str] | Search for Tokens in the specified states (optional)
limit = 5 # int | maximum number of results to return per page (1 or more) (optional) (default to 5)
offset = 0 # int | number of items to skip before starting to collect the result set (optional) (default to 0)

try:
    # Get tokens
    api_response = api_instance.tokens_get(token_hash=token_hash, project_id=project_id, expires=expires, states=states, limit=limit, offset=offset)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TokensApi->tokens_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token_hash** | **str**| Token identified by SHA256 hash | [optional] 
 **project_id** | **str**| Project identified by universally unique identifier | [optional] 
 **expires** | **str**| Search for tokens with expiry time lesser than the specified expiration time | [optional] 
 **states** | [**list[str]**](str.md)| Search for Tokens in the specified states | [optional] 
 **limit** | **int**| maximum number of results to return per page (1 or more) | [optional] [default to 5]
 **offset** | **int**| number of items to skip before starting to collect the result set | [optional] [default to 0]

### Return type

[**Tokens**](Tokens.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tokens_refresh_post**
> Tokens tokens_refresh_post(body, project_id=project_id, scope=scope)

Refresh tokens for an user

Request to refresh OAuth tokens for an user 

### Example
```python
from __future__ import print_function
import time
from fabric_cm.credmgr.swagger_client import TokensApi
from fabric_cm.credmgr.swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = TokensApi()
body = swagger_client.Request() # Request | 
project_id = 'project_id_example' # str | Project identified by universally unique identifier (optional)
scope = 'all' # str | Scope for which token is requested (optional) (default to all)

try:
    # Refresh tokens for an user
    api_response = api_instance.tokens_refresh_post(body, project_id=project_id, scope=scope)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TokensApi->tokens_refresh_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Request**](Request.md)|  | 
 **project_id** | **str**| Project identified by universally unique identifier | [optional] 
 **scope** | **str**| Scope for which token is requested | [optional] [default to all]

### Return type

[**Tokens**](Tokens.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tokens_revoke_list_get**
> RevokeList tokens_revoke_list_get(project_id=project_id)

Get token revoke list i.e. list of revoked identity token hashes

Get token revoke list i.e. list of revoked identity token hashes for a user in a project 

### Example
```python
from __future__ import print_function
import time
from fabric_cm.credmgr.swagger_client import TokensApi
from fabric_cm.credmgr.swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = TokensApi()
project_id = 'project_id_example' # str | Project identified by universally unique identifier (optional)

try:
    # Get token revoke list i.e. list of revoked identity token hashes
    api_response = api_instance.tokens_revoke_list_get(project_id=project_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TokensApi->tokens_revoke_list_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project identified by universally unique identifier | [optional] 

### Return type

[**RevokeList**](RevokeList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tokens_revoke_post**
> Status200OkNoContent tokens_revoke_post(body)

Revoke a token for an user

Request to revoke a token for an user 

### Example
```python
from __future__ import print_function
import time
from fabric_cm.credmgr.swagger_client import TokensApi, Request
from fabric_cm.credmgr.swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = TokensApi()
body = Request() # Request | 

try:
    # Revoke a token for an user
    api_response = api_instance.tokens_revoke_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TokensApi->tokens_revoke_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Request**](Request.md)|  | 

### Return type

[**Status200OkNoContent**](Status200OkNoContent.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tokens_revokes_post**
> Status200OkNoContent tokens_revokes_post(body)

Revoke a token

Request to revoke a token 

### Example
```python
from __future__ import print_function
import time
from fabric_cm.credmgr.swagger_client import TokensApi
from fabric_cm.credmgr.swagger_client.models import TokenPost
from fabric_cm.credmgr.swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = TokensApi()
body = TokenPost() # TokenPost | 

try:
    # Revoke a token
    api_response = api_instance.tokens_revokes_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TokensApi->tokens_revokes_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TokenPost**](TokenPost.md)|  | 

### Return type

[**Status200OkNoContent**](Status200OkNoContent.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tokens_validate_post**
> Status200OkNoContent tokens_validate_post(body)

Validate an identity token issued by Credential Manager

Validate an identity token issued by Credential Manager 

### Example
```python
from __future__ import print_function
import time
from fabric_cm.credmgr.swagger_client import TokensApi, TokenPost
from fabric_cm.credmgr.swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = TokensApi()
body = TokenPost() # TokenPost | 

try:
    # Validate an identity token issued by Credential Manager
    api_response = api_instance.tokens_validate_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TokensApi->tokens_validate_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TokenPost**](TokenPost.md)|  | 

### Return type

[**Status200OkNoContent**](Status200OkNoContent.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

