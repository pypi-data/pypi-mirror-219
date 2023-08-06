from adafri.utils.utils import JsonEncoder, DictUtils, get_object_model_class
from dataclasses import dataclass
import json
import pydash
from firebase_admin.firestore import firestore
from google.cloud.firestore_v1.base_query import FieldFilter, And
import os
from ..auth.firebase_auth import FirestoreApp

def getTimestamp():
    return firestore.SERVER_TIMESTAMP;

@dataclass(init=False)
class FirebaseCollectionBase:
    # _db: firestore.Client = None;
    # _fields_props = None;
    # _collection_name = None;

    def __init__(self, collection_name=None, db: firestore.Client=None, fields=None, fields_props=None, id=None):
        self.collection_name = collection_name;
        self.db = db;
        self.id = id;
        if self.db is None:
            self.db = FirestoreApp().firestore_client()
        self.fields = fields;
        self.fields_props = fields_props;
        
    def print_db(self):
        print('db prtiny',self.db)

    def setFields(self, fields):
        self.fields_props = fields;
    
    def generate_model(self, _key_):
        user = {};
        props = self.fields_props
        for k in DictUtils.get_keys(props):
            user[k] = props[k][_key_];
        return user;

    def collection(self):
        return self.db.collection(self.collection_name)

    def document_reference(self, _id=None) -> 'firestore.DocumentReference':
        id = _id;
        if id is None:
            if self.id is not None:
                id = self.id;
        return self.collection().document(id);

    # def get(self, id):
    #     if id is None or bool(id) is False:
    #          return None;
    #     doc = self.document_reference(id).get();
    #     if doc.exists is False:
    #         return None;
    #     return doc.to_dict();
    
    def update(self, id, data, merge=True):
        if id is None or bool(id) is False:
            return None;
        doc = self.document_reference(id);
        if doc.get().exists is False:
            return None;
        try:
            doc.set(data, merge=merge);
            return data;
        except:
            return None
    
    def remove(self, id):
        if id is None or bool(id) is False:
             return None;
        doc = self.document_reference(id);
        if doc.get().exists is False:
            return None;
        try:
            doc.delete();
            return id;
        except:
            return None

    def custom_query(self, query_params, first=True, limit: int=None):
        i = 0;
        dynamic_query = None;
        filters = []
        while i < len(query_params):
            query = query_params[i];
            
            key = None;
            if 'key' in query:
                key = query['key'];
            
            comparator = None;
            if 'comp' in query:
                comparator = query['comp']

            value = None;
            if 'value' in query:
                value = query['value'];
            if None not in [key, comparator, value]:
                filters.append(FieldFilter(key, comparator, value))
            i+=1;

        and_filter = And(filters=filters)
        dynamic_query = self.collection().where(filter=and_filter)
        if dynamic_query is None:
            return None
        _limit = limit
        if _limit is not None and _limit > 0 or first:
            if _limit is None:
                _limit = 1
            dynamic_query = dynamic_query.limit(_limit)
        
        data = []
        for stream in dynamic_query.stream():
            data.append({"id": stream.id, **stream.to_dict()});
        if first is False:
            if len(data) == 0:
                return []
            return data;
        else:
            if len(data) == 0:
                return None;
            return data[0]
        
    
    
    def to_json(self, _fields=None):
        fields = self.fields;
        if _fields is not None and type(_fields) is list and len(_fields)>0:
            fields = _fields;
        json_object, keys = get_object_model_class({}, self, self.fields_props);
        if fields is None or type(fields) is not list or len(fields)==0:
            return json_object
        return pydash.pick(json_object, fields)
    


