from dataclasses import dataclass
from .....utils import DictUtils

TOKEN_COLLECTION = "clients_token_collection";
@dataclass
class TokenFields:
    id = "id"
    client_id = "client_id"
    uid = "uid"
    token_type = "token_type"
    access_token = "access_token"
    refresh_token = "refresh_token"
    scopes = "scopes"
    scope = "scope"
    expires_in = "expires_in"
    expired_at = "expired_at"
    expires = "expires"

    @staticmethod
    def keys():
        return DictUtils.get_keys(TokenFieldsProps);

    @staticmethod
    def filtered_keys(field, condition=True):
        mutable = DictUtils.filter(TokenFieldsProps, DictUtils.get_keys(TokenFieldsProps), field, condition)
        return DictUtils.get_keys(mutable);

TokenFieldsProps = {
    TokenFields.id: {
        "type": str,
        "required": True,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "default_value": "",
        "pickable": True
    },
    TokenFields.client_id: {
        "type": str,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "default_value": "",
        "pickable": True
    },
    TokenFields.scope: {
        "type": str,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "default_value": "",
        "pickable": True
    },
    TokenFields.uid: {
        "type": str,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "default_value": "",
        "pickable": True
    },
    TokenFields.token_type: {
        "type": str,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "default_value": "",
        "pickable": True
    },
    TokenFields.access_token: {
        "type": str,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "default_value": "",
        "pickable": True
    },
    TokenFields.refresh_token: {
        "type": str,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "default_value": "",
        "pickable": True
    },
    TokenFields.scopes: {
        "type": list,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "default_value": "",
        "pickable": True
    },
    TokenFields.expires: {
        "type": str,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "default_value": "",
        "pickable": True
    },
    TokenFields.expires_in: {
        "type": int,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "default_value": 3600,
        "pickable": True
    },
    TokenFields.expired_at: {
        "type": float,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "default_value": 0,
        "pickable": True
    },
}

STANDARD_FIELDS = TokenFields.filtered_keys('pickable', True)