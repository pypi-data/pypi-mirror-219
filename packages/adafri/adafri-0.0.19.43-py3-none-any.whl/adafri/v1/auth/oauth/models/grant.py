from .....utils import ArrayUtils, DictUtils, Crypto, get_object_model_class, init_class_kwargs
from ....base.firebase_collection import (FirebaseCollectionBase, getTimestamp)
from .grant_fields import GrantFields, GrantFieldsProps, STANDARD_FIELDS, GRANT_COLLECTION
from .....utils.response import ApiResponse, Error, ResponseStatus, StatusCode
from typing import Any
from dataclasses import dataclass
from authlib.oauth2.rfc6749 import AuthorizationCodeMixin
from authlib.oauth2.rfc6749 import grants
from authlib.common.urls import add_params_to_uri
from authlib.oauth2.rfc6749.util import list_to_scope, scope_to_list
from authlib.oauth2.rfc6749.errors import AccessDeniedError
from ....user import User
import pydash
from authlib.oidc.core.grants import (
    OpenIDCode as _OpenIDCode,
    OpenIDImplicitGrant as _OpenIDImplicitGrant,
    OpenIDHybridGrant as _OpenIDHybridGrant,
)
from authlib.oidc.core import UserInfo
from werkzeug.security import gen_salt

import os
@dataclass(init=False)
class OAuthGrant(AuthorizationCodeMixin, FirebaseCollectionBase):
    id: str
    code: str
    uid: str
    client_id: str
    redirect_uri: str
    scopes: list[str]
    scope: str
    expires: str
    code_challenge: str
    code_challenge_method: str
    
    def __init__(self, grant=None, **kwargs):
        (cls_object, keys, data_args) = init_class_kwargs(self, grant, STANDARD_FIELDS, GrantFieldsProps, GRANT_COLLECTION, ['id'], **kwargs)
        super().__init__(**data_args);
        for key in keys:
            setattr(self, key, cls_object[key]) 
        # kwargs['fields'] = STANDARD_FIELDS
        # kwargs['fields_props'] = GrantFieldsProps
        # collection_name = getattr(kwargs, 'collection_name', None)
        # documentId = getattr(cls_object, 'id', None)
        # if documentId is not None:
        #     kwargs['documentId'] = documentId;
        # if collection_name is None:
        #     kwargs['collection_name'] = GRANT_COLLECTION;
        


    @staticmethod
    def generate_model(_key_="default_value"):
        grant = {};
        props = GrantFieldsProps
        for k in DictUtils.get_keys(props):
            grant[k] = props[k][_key_];
        return grant;

    @staticmethod
    def from_dict(grant: Any=None, db=None, collection_name=None) -> 'OAuthGrant':
        cls_object, keys = get_object_model_class(grant, OAuthGrant, GrantFieldsProps);
        _client = OAuthGrant(cls_object, db=db, collection_name=collection_name)
        return _client

    def query(self, query_params: list, first=False, limit=None):
        query_result = [];
        query_result = self.custom_query(query_params, first=first, limit=limit)
        if bool(query_result):
            if first:
                return OAuthGrant.from_dict(grant=query_result, db=self.db, collection_name=self.collection_name)
            else:
                for doc in query_result:
                    query_result.append(OAuthGrant.from_dict(client=doc, db=self.db, collection_name=self.collection_name))
                return query_result
        if first:
                return None
        return [];

    def get(self) -> 'OAuthGrant':
        if bool(self.id):
            doc = self.document_reference(self.id).get();
            if doc.exists is False:
                return None;
            return OAuthGrant.from_dict(doc.to_dict(), db=self.db, collection_name=self.collection_name);
        if bool(self.client_id):
            return self.query([{"key": "client_id", "comp": "==", "value": self.client_id}])

    @staticmethod
    def generate(**kwargs) -> 'ApiResponse':
        data_dict = DictUtils.pick_fields(kwargs, GrantFields.filtered_keys('mutable', True));
        authorization_code_model = OAuthGrant.from_dict(DictUtils.merge_dict(data_dict, OAuthGrant.generate_model()));
        
        if bool(authorization_code_model.to_json()) is False:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error("Empty request","INVALID_REQUEST", 1)).to_json()
        
        if bool(authorization_code_model.code) is False:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error("name required","INVALID_REQUEST", 1));

        authorization_code_model.id = Crypto().generate_id(authorization_code_model.code+"~"+authorization_code_model.client_id);
        return ApiResponse(ResponseStatus.OK, StatusCode.status_200, authorization_code_model, None);

    def get_redirect_uri(self):
        return self.redirect_uri
    
    def get_scope(self):
       return self.scope
    
    @staticmethod
    def create(**kwargs):
        authorization_code = OAuthGrant().generate(**kwargs);
        if authorization_code.status == ResponseStatus.ERROR:
            return authorization_code
        
        docRef = OAuthGrant(authorization_code.data).document_reference();
        if docRef.get().exists:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(f"Location with name {authorization_code.id} already exist","INVALID_REQUEST", 1));
        
        authorization_code_model: OAuthGrant = authorization_code.data;
        docRef.set({**authorization_code_model.to_json(), "createdAt": getTimestamp()}, merge=True);
        created_campaign = authorization_code_model.get()
        return ApiResponse(ResponseStatus.OK, StatusCode.status_200, created_campaign.to_json(), None);
    
    def update(self, data):
        try:
            last_value = self.to_json();
            filtered_value = pydash.pick(data, GrantFields.filtered_keys('editable', True));
            new_value = DictUtils.merge_dict(filtered_value, self.to_json());
            changed_fields = DictUtils.get_changed_field(last_value, new_value);
            data_update = DictUtils.dict_from_keys(filtered_value, changed_fields);
            if bool(data_update) is False:
                return None;
            self.document_reference().set(data_update, merge=True)
            return DictUtils.dict_from_keys(self.get().to_json(), changed_fields);
        except Exception as e:
            print(e)
            return None;
    
    def remove(self):
        try:
            if self.id is None:
                return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(f"Cannot identify Authorization code with id {self.id} to delete","INVALID_REQUEST", 1));
            deleted = self.document_reference().delete();
            return ApiResponse(ResponseStatus.OK, StatusCode.status_200, {"message": f"Authorization code {self.id} deleted"}, None);
        except:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(f"An error occurated while removing authorization code with id {self.id}","INVALID_REQUEST", 1));

    

class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = [
        'client_secret_basic',
        'client_secret_post',
        'none'
    ]
    def save_authorization_code(self, code, request):
        code_challenge = request.data.get('code_challenge')
        code_challenge_method = request.data.get('code_challenge_method')
        redirect_uri = request.redirect_uri;
        if request.args.get("redirect_uri") is not None:
            redirect_uri = request.args.get("redirect_uri");
        if redirect_uri is None:
            default_redirect_uri =os.environ.get('DEFAULT_REDIRECT_URI')
            redirect_uri = default_redirect_uri
        model = {
            "client_id": request.client.client_id,
            "code": code,
            "redirect_uri": redirect_uri,
            "scopes": ArrayUtils.join_string_to_array(request.args.get("scope"), ","),
            "scope": request.args.get("scope"),
            "uid": request.user.uid,
            "code_challenge": code_challenge,
            "code_challenge_method": code_challenge_method
        }
        auth_code_request = OAuthGrant.create(**model)
        auth_code = auth_code_request.data
        return auth_code

    
    def query_authorization_code(self, code, client):
        query_params = [{"key": GrantFields.code, "comp": "==","value": code}, {"key": GrantFields.client_id, "comp": "==","value": client.client_id}]
        auth_code = OAuthGrant().query(query_params=query_params, first=True)
        #if auth_code and not auth_code.is_expired():
        return auth_code

    def delete_authorization_code(self, authorization_code):
        remove = OAuthGrant(authorization_code.to_json()).remove()
        print('removing authorization code', authorization_code.id)

    def authenticate_user(self, authorization_code):
        return User({"uid": authorization_code.uid}).get()
    
    def create_authorization_response(self, redirect_uri: str, grant_user):
        if not grant_user:
            raise AccessDeniedError(state=self.request.state, redirect_uri=redirect_uri)

        self.request.user = grant_user
        code = self.generate_authorization_code()
        element = code;
        element_key = "code";

        self.save_authorization_code(code, self.request)
        if self.request.response_type=="token":
            element_key = "access_token"
            token = self.generate_token(self.request.user, self.request.scope, self.GRANT_TYPE, 3600, True);
            self.save_token(token);
            element = token['access_token']

        params = [(element_key, element)]
        if self.request.state:
            params.append(('state', self.request.state))
        uri = add_params_to_uri(redirect_uri, params)
        headers = [('Location', uri)]
        return 302, '', headers
    


DUMMY_JWT_CONFIG = {
    'key': 'secret-key',
    'alg': 'HS256',
    'iss': 'https://auth.adafri.dev.org',
    'exp': 3600,
}

def exists_nonce(nonce, req):
    query_params = [{"key": GrantFields.nonce, "comp": "==","value": nonce}, {"key": GrantFields.client_id, "comp": "==","value": req.client_id}]
    exists = OAuthGrant().query(query_params=query_params, first=True)
    return bool(exists)


def generate_user_info(user, scope):
    return UserInfo(sub=str(user.id), name=user.username)



def create_authorization_code(client, grant_user, request):
    code = gen_salt(48)
    nonce = request.data.get('nonce')
    grant = {
        "code":code,
        "client_id": client.client_id,
        "redirect_uri": request.redirect_uri,
        "scope":request.scope,
        "uid": grant_user.id,
        "nonce": nonce,
    }
    auth_code = OAuthGrant.create(**grant)
    return auth_code.data

class OpenIDAuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    # RESPONSE_TYPES = set({"code"})
    TOKEN_ENDPOINT_AUTH_METHODS = [
        'client_secret_basic',
        'client_secret_post',
        'none'
    ]
    def save_authorization_code(self, code, request):
        code_challenge = request.data.get('code_challenge')
        code_challenge_method = request.data.get('code_challenge_method')
        redirect_uri = request.redirect_uri;
        nonce = request.data.get('nonce')
        if request.args.get("redirect_uri") is not None:
            redirect_uri = request.args.get("redirect_uri");
        if redirect_uri is None:
            default_redirect_uri =os.environ.get('DEFAULT_REDIRECT_URI')
            redirect_uri = default_redirect_uri
        model = {
            "client_id": request.client.client_id,
            "code": code,
            "redirect_uri": redirect_uri,
            "scopes": ArrayUtils.join_string_to_array(request.args.get("scope"), ","),
            "scope": request.args.get("scope"),
            "uid": request.user.uid,
            "code_challenge": code_challenge,
            "code_challenge_method": code_challenge_method,
            "nonce": nonce,
        }
        auth_code_request = OAuthGrant.create(**model)
        auth_code = auth_code_request.data
        return auth_code
    
    def create_authorization_code(self, client, grant_user, request):
        return create_authorization_code(client, grant_user, request)
    
    def parse_authorization_code(self, code, client):
        query_params = [{"key": GrantFields.code, "comp": "==","value": code}, {"key": GrantFields.client_id, "comp": "==","value": client.client_id}]
        auth_code = OAuthGrant().query(query_params=query_params, first=True)
        #if auth_code and not auth_code.is_expired():
        return auth_code
   
    def query_authorization_code(self, code, client):
        query_params = [{"key": GrantFields.code, "comp": "==","value": code}, {"key": GrantFields.client_id, "comp": "==","value": client.client_id}]
        auth_code = OAuthGrant().query(query_params=query_params, first=True)
        #if auth_code and not auth_code.is_expired():
        return auth_code
    
    def delete_authorization_code(self, authorization_code):
        remove = OAuthGrant(authorization_code.to_json()).remove()
        print('removing authorization code', authorization_code.id)

    def authenticate_user(self, authorization_code):
        return User({"uid": authorization_code.uid}).get()
    
class OpenIDCode(_OpenIDCode):
    def exists_nonce(self, nonce, request):
        return exists_nonce(nonce, request)

    def get_jwt_config(self, grant):
        return DUMMY_JWT_CONFIG

    def generate_user_info(self, user, scope):
        return generate_user_info(user, scope)


class OpenIDImplicitGrant(_OpenIDImplicitGrant):
    def exists_nonce(self, nonce, request):
        return exists_nonce(nonce, request)

    def get_jwt_config(self, grant):
        return DUMMY_JWT_CONFIG

    def generate_user_info(self, user, scope):
        return generate_user_info(user, scope)


class OpenIDHybridGrant(_OpenIDHybridGrant):
    def create_authorization_code(self, client, grant_user, request):
        return create_authorization_code(client, grant_user, request)

    def exists_nonce(self, nonce, request):
        return exists_nonce(nonce, request)

    def get_jwt_config(self):
        return DUMMY_JWT_CONFIG

    def generate_user_info(self, user, scope):
        return generate_user_info(user, scope)
    

