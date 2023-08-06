from ...base.firebase_collection import FirebaseCollectionBase
from ....utils import (DictUtils, get_object_model_class, init_class_kwargs)
from ....utils.response import ApiResponse, Error, ResponseStatus, StatusCode
from .account_fields import AccountFields, AccountFieldProps, STANDARD_FIELDS, ACCOUNT_COLLECTION
from typing import Any
from dataclasses import dataclass
import pydash

@dataclass(init=False)
class Account(FirebaseCollectionBase):
    id: str
    aacid: str
    account_value: int
    creationDate: int
    creationDateString: str
    name: str
    owner: str
    owner_email: str
    status: str
    totalClics: int
    totalCosts: int
    totalImpressions: int
    usedPackTest: bool

    def __init__(self, account, **kwargs):
        (cls_object, keys, data_args) = init_class_kwargs(self, account, STANDARD_FIELDS, AccountFieldProps, ACCOUNT_COLLECTION, ['id'], **kwargs)
        super().__init__(**data_args);
        for key in keys:
            setattr(self, key, cls_object[key]) 


    @staticmethod
    def generate_model(_key_="default_value"):
        user = {};
        props = AccountFieldProps
        for k in DictUtils.get_keys(props):
            user[k] = props[k][_key_];
        return user;

    @staticmethod
    def from_dict(account: Any, db=None, collection_name=None) -> 'Account':
        cls_object, keys = get_object_model_class(account, Account, AccountFieldProps);
        if AccountFields.aacid in cls_object and bool(cls_object[AccountFields.aacid]) is False:
            if AccountFields.id in cls_object and bool(cls_object[AccountFields.id]):
                cls_object[AccountFields.aacid] = cls_object[AccountFields.id]
        _account = Account(cls_object, db=db, collection_name=collection_name)
        return _account
    
    
    def get(self):
        id = self.aacid;
        if bool(id) is False:
            if self.id is None:
                return None;
            id = self.id;
        if bool(id) is None:
            return None;
    
        doc = self.document_reference().get();
        if doc.exists is False:
            return None;
        data = {"id": doc.id, **doc.to_dict()}
        return Account.from_dict(data, db=self.db, collection_name=self.collection_name);

    def query(self, query_params: list, first=False, limit=None):
        query_result = [];
        query_result = self.custom_query(query_params, first=first, limit=limit)
        if bool(query_result):
            if first:
                return Account.from_dict(account=query_result, db=self.db, collection_name=self.collection_name)
            else:
                for doc in query_result:
                    query_result.append(Account.from_dict(account=doc, db=self.db, collection_name=self.collection_name))
                return query_result
        if first:
                return None
        return [];

    def getAccount(self):
            account = self.get(self.aacid);
            if account is None:
                return None;
            return account.to_json();

    def update(self, data):
        try:
            last_value = self.to_json();
            filtered_value = pydash.pick(data, AccountFields.filtered_keys('editable', True));
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

    def remove(self, only_mark_as_removed=True):
        try:
            if self.id is None:
                return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(f"Cannot identify Account with id {self.id}","INVALID_REQUEST", 1));
            if only_mark_as_removed:
                self.document_reference().set({"is_removed": True})
            else:
                self.document_reference().delete();
            return ApiResponse(ResponseStatus.OK, StatusCode.status_200, {"message": f"Account {self.id} deleted"}, None);
        except:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(f"An error occurated while removing authorization code with id {self.id}","INVALID_REQUEST", 1));


    
   