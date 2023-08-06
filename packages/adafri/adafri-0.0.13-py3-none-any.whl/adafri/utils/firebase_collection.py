from utils.utils import JsonEncoder, DictUtils
from dataclasses import dataclass
import json
import pydash

@dataclass
class FirebaseCollectionBase:

    def __init__(self, collection_name=None, db=None, fields=None):
        self.collection_name = collection_name;
        self.db = db;
        self.fields_props = fields;
        

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

    def document_reference(self, uid):
        return self.collection(self.collection_name).document(uid);
    
    
    def to_json(self, fields=None):
        if fields is None or type(fields) is not list:
            return json.loads(JsonEncoder().encode(self));
    
        return pydash.pick(json.loads(JsonEncoder().encode(self)), fields)
    


