from .....utils import DictUtils, Crypto, get_object_model_class, pydash, init_class_kwargs
from ....base.firebase_collection import (FirebaseCollectionBase, getTimestamp)
from .token_fields import TokenFields, TokenFieldsProps, STANDARD_FIELDS, TOKEN_COLLECTION
from .....utils.response import ApiResponse, Error, ResponseStatus, StatusCode
from typing import Any
from dataclasses import dataclass
from ....user import User
from authlib.oauth2.rfc7009 import RevocationEndpoint
from authlib.oauth2.rfc6750 import BearerTokenValidator
from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc6749 import TokenMixin
from authlib.oauth2.rfc6750 import BearerTokenGenerator
from datetime import datetime, timedelta
import json
from flask import abort, Response

@dataclass(init=False)
class OAuthToken(TokenMixin, FirebaseCollectionBase):
    id: str
    client_id: str
    uid: str
    token_type: str
    access_token: str
    refresh_token: str
    scopes: list[str]
    scope: str
    expired_at: str
    expires_in: int
    revoked: bool
    
    def __init__(self, token=None, **kwargs):
        (cls_object, keys, data_args) = init_class_kwargs(self, token, STANDARD_FIELDS, TokenFieldsProps, TOKEN_COLLECTION, ['id'], **kwargs)
        super().__init__(**data_args);
        for key in keys:
            setattr(self, key, cls_object[key]) 


    @staticmethod
    def generate_model(_key_="default_value"):
        grant = {};
        props = TokenFieldsProps
        for k in DictUtils.get_keys(props):
            grant[k] = props[k][_key_];
        return grant;

    @staticmethod
    def from_dict(token: Any=None, db=None, collection_name=None) -> 'OAuthToken':
        cls_object, keys = get_object_model_class(token, OAuthToken, TokenFieldsProps);
        _client = OAuthToken(cls_object, db=db, collection_name=collection_name)
        return _client

    def query(self, query_params: list, first=False, limit=None):
        query_result = [];
        query_result = self.custom_query(query_params, first=first, limit=limit)
        if bool(query_result):
            if first:
                return OAuthToken.from_dict(token=query_result, db=self.db, collection_name=self.collection_name)
            else:
                for doc in query_result:
                    query_result.append(OAuthToken.from_dict(token=doc, db=self.db, collection_name=self.collection_name))
                return query_result
        if first:
                return None
        return [];

    def get(self) -> 'OAuthToken':
        if bool(self.id):
            doc = self.document_reference().get();
            if doc.exists is False:
                return None;
            return OAuthToken.from_dict(doc.to_dict(), db=self.db, collection_name=self.collection_name);
        if bool(self.client_id):
            return self.query([{"key": "client_id", "comp": "==", "value": self.client_id}])

    @staticmethod
    def generate(**kwargs) -> 'ApiResponse':
        data_dict = DictUtils.pick_fields(kwargs, TokenFields.filtered_keys('mutable', True));
        token_model = OAuthToken.from_dict(DictUtils.merge_dict(data_dict, OAuthToken.generate_model()));
        
        if bool(token_model.to_json()) is False:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error("Empty request","INVALID_REQUEST", 1)).to_json()
        
        if bool(token_model.access_token) is False:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error("name required","INVALID_REQUEST", 1));

        token_model.id = Crypto().generate_id(token_model.access_token+"~"+token_model.client_id);
        return ApiResponse(ResponseStatus.OK, StatusCode.status_200, token_model, None);
    

    def save(self, token, request):
        model = {**token, "client_id": request.client.client_id, "uid": request.user.uid}
        token_generate = OAuthToken.generate(**model);
        if token_generate.status == ResponseStatus.ERROR:
            return token_generate
        docRef = OAuthToken(token_generate.data.to_json()).document_reference();
        if docRef.get().exists:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(f"Location with name {token_generate.data.id} already exist","INVALID_REQUEST", 1));
        
        token_model: OAuthToken = token_generate.data;
        docRef.set({**token_model.to_json(), "createdAt": getTimestamp()}, merge=True);
        created_token = token_model.get()
        return ApiResponse(ResponseStatus.OK, StatusCode.status_200, created_token.to_json(), None);
    
    def update(self, data):
        try:
            last_value = self.to_json();
            filtered_value = pydash.pick(data, TokenFields.filtered_keys('editable', True));
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
                return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(f"Cannot identify token with id {self.id} to delete","INVALID_REQUEST", 1));
            deleted = self.document_reference().delete();
            return ApiResponse(ResponseStatus.OK, StatusCode.status_200, {"message": f"Token {self.id} deleted"}, None);
        except:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(f"An error occurated while removing authorization code with id {self.id}","INVALID_REQUEST", 1));


    def is_expired(self):
        return datetime.fromisoformat(self.expired_at) < datetime.now()
    
    def is_revoked(self):
        return self.revoked
    

class TokenValidator(BearerTokenValidator):
    def authenticate_token(self, token_string):
        token_request = OAuthToken().query([{"key":"access_token", "comp": "==", "value": token_string}], True)
        return token_request
    
    def validate_token(self, token, scopes, request):
        token_scopes = json.loads(token.scope);
        insufficient = self.scope_insufficient(token_scopes, scopes);
        if insufficient:
            response = ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error("Insufficient privilegies","INVALID_REQUEST", 1)).to_json()
            return abort(Response(response=json.dumps(response), status=401, mimetype='application/json'))        
        return None

class TokenRevocationEndpoint(RevocationEndpoint):
    def query_token(self, token, token_type_hint, client):
        q: list = OAuthToken().query([{"key":"client_id", "comp": "==", "value": client.clent_id}], False)
        if token_type_hint == 'access_token':
            return pydash.find(q, lambda x: x.access_token==token);
        elif token_type_hint == 'refresh_token':
            return pydash.find(q, lambda x: x.refresh_token==token);
        # without token_type_hint
        item = pydash.find(q, lambda x: x.access_token==token);
        if item:
            return item
        return pydash.find(q, lambda x: x.refresh_token==token);

    def revoke_token(self, _token):
        token = OAuthToken.from_dict(_token);
        token.revoked = True
        token.update(_token);

class RefreshTokenGrant(grants.RefreshTokenGrant):
    def authenticate_refresh_token(self, refresh_token):
        token = OAuthToken().query([{"key":"refresh_token", "comp": "==", "value": refresh_token}], True);
        return token;
        # if token and token.is_refresh_token_active():
        #     return token

    def authenticate_user(self, credential):
        return User.get(credential.user_id)

    # def revoke_old_credential(self, credential):
    #     credential.revoked = True
    #     db.session.add(credential)
    #     db.session.commit()


DEFAULT_EXPIRES_IN = 3600
class TokenGenerator(BearerTokenGenerator):
    @staticmethod
    def generate(grant_type, client, user=None, scope=None, expires_in=None, include_refresh_token=True):
        if expires_in is None:
            expires_in = DEFAULT_EXPIRES_IN
        expires_at = datetime.now() + timedelta(seconds=DEFAULT_EXPIRES_IN)
        token = {'token_type': 'Bearer', "client_id": client.client_id, "uid": user.uid, 'scope': scope, 'expires_in': expires_in, "grant_type": grant_type, 'expired_at': expires_at.isoformat()}
        access_token = Crypto().generate_token("access_token~"+json.dumps(token));
        token['access_token'] = access_token;
        if include_refresh_token:
            token['refresh_token'] = Crypto().generate_token("refresh_token~"+json.dumps(token));
        return token