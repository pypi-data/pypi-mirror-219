from utils.utils import ArrayUtils, JsonEncoder, DictUtils, Crypto
from .client_fields import ClientFields, ClientFieldProps
from utils.response import ApiResponse, Error, ResponseStatus, StatusCode
from werkzeug.security import gen_salt
import time
from typing import List
from typing import Any
from dataclasses import dataclass
import json
import pydash
from authlib.oauth2.rfc6749 import ClientMixin
import secrets

@dataclass
class Client(ClientMixin):
    id: str
    name: str
    uid: str
    description: str
    client_id: str
    client_secret: str
    uri: str
    grant_types: list[str]
    response_types: list[str]
    token_endpoint_auth_method: str
    redirect_uris: list[str]
    scopes: list[str]
    client_id_issued_at: int
    createdAt: any
    allowed_redirect_uris: list[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Client':
        _id = str(DictUtils.pick(obj, ClientFields.id, str));
        _name = str(DictUtils.pick(obj, ClientFields.name, str));
        _uid = str(DictUtils.pick(obj, ClientFields.uid, str));
        _description = str(DictUtils.pick(obj, ClientFields.description, str));
        _client_id = str(DictUtils.pick(obj, ClientFields.client_id, str));
        _client_secret = str(DictUtils.pick(obj, ClientFields.client_secret, str));
        _uri = str(DictUtils.pick(obj, ClientFields.uri, str));
        _grant_types = [y for y in DictUtils.pick(obj, ClientFields.grant_types, list)]
        _response_types = [y for y in DictUtils.pick(obj, ClientFields.response_types, list)]
        _token_endpoint_auth_method = str(DictUtils.pick(obj, ClientFields.token_endpoint_auth_method, str));
        _redirect_uris = [y for y in DictUtils.pick(obj, ClientFields.redirect_uris, list)]
        _scopes = [y for y in DictUtils.pick(obj, ClientFields.scopes, list)]
        _client_id_issued_at = int(str(DictUtils.pick(obj, ClientFields.client_id_issued_at, int)));
        _createdAt = str(DictUtils.pick(obj, ClientFields.created_at, str, ""));
        _allowed_redirect_uris = [y for y in DictUtils.pick(obj, ClientFields.allowed_redirect_uris, list)]
        if bool(_allowed_redirect_uris) is False:
            _allowed_redirect_uris = _redirect_uris
        return Client(_id, _name, _uid, _description, _client_id, _client_secret, _uri, _grant_types,  _response_types, _token_endpoint_auth_method, _redirect_uris, _scopes, _client_id_issued_at, _createdAt, _allowed_redirect_uris)


    @staticmethod
    def generate_model():
        user = {};
        for k in DictUtils.get_keys(ClientFieldProps):
            _key_ = 'default_value';
            user[k] = ClientFieldProps[k][_key_];
        return user;

    @staticmethod
    def generate(**kwargs) -> 'ApiResponse':
        data_dict = DictUtils.pick_fields(kwargs, ClientFields.filtered_keys('mutable', True));
        print('data_dict:', data_dict)
        client_model = Client.from_dict(DictUtils.merge_dict(data_dict, Client.generate_model()));
        
        if bool(client_model.to_json()) is False:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error("Empty request","INVALID_REQUEST", 1)).to_json()
        
        if bool(client_model.name) is False:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error("name required","INVALID_REQUEST", 1));
        
        if bool(client_model.uid) is False:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error("uid required","INVALID_REQUEST", 1));

        client_model.id = Crypto().generate_id(client_model.name+"~"+client_model.uid);
        client_model.client_id = gen_salt(24)
        client_model.client_id_issued_at = int(time.time())
        
        if client_model.token_endpoint_auth_method == 'none':
            client_model.client_secret = ''
        else:
            client_model.client_secret = gen_salt(48)
        return ApiResponse(ResponseStatus.OK, StatusCode.status_200, client_model.to_json(), None);

    def to_json(self, fields=None):
        if fields is None or type(fields) is not list:
            return json.loads(JsonEncoder().encode(self));
        return pydash.pick(json.loads(JsonEncoder().encode(self)), fields)
    
    
    # def get_default_redirect_uri(self):
    #     return f"{baseUrl}/auth/challenge_success"
    
    def check_response_type(self, response_type):
        return response_type in self.response_types
    
    def check_client_secret(self, client_secret):
        return secrets.compare_digest(self.client_secret, client_secret)
    
    def check_endpoint_auth_method(self, method, endpoint):
        if endpoint == 'token':
            # if client table has ``token_endpoint_auth_method``
            return self.token_endpoint_auth_method == method
        return True
    
    def check_grant_type(self, grant_type):
        return grant_type in self.grant_types
    
    def get_allowed_scope(self, scope):
        if not scope:
            return ''
        allowed = self.scopes
        scopes = ArrayUtils.array_to_string([s for s in json.loads(scope) if s in allowed])
        return scopes
    
    def check_redirect_uri(self, redirect_uri):
        return redirect_uri in self.allowed_redirect_uris
