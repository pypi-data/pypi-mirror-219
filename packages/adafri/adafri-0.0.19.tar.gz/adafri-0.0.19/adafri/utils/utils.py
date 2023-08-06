import json
import pydash
from typing import Iterable
import hashlib
from cryptography.fernet import Fernet
import os
import base64
from datetime import date

hash = hashlib.sha1(str(os.getenv('CRYPTO_KEY')).encode())
ENCRYPTION_KEY = base64.b64encode(hash.hexdigest()[:32].encode()).decode();

class Crypto:

    print(ENCRYPTION_KEY)
    print(hash.hexdigest())
    fernet = Fernet(ENCRYPTION_KEY);
    def encrypt(self, message:str):
        return self.fernet.encrypt(message.encode()).decode();

    def decrypt(self, encrypted:str):
        return self.fernet.decrypt(encrypted).decode();

    def hash(self, message:str):
        return hashlib.sha256(str(message).encode()).hexdigest();
    
    def generate_id(self, message:str):
        return hashlib.md5(str(message).encode()).hexdigest();

    def generate_token(self, message:str):
        return self.encrypt("token~"+hashlib.md5(str(message).encode()).hexdigest())

class RequestFields:
    data = 'data';
    fields = 'fields';

def get_request_fields(field_string, fields, default_fields):
    request_fields =[];
    load_fields = ArrayUtils.join_string_to_array(field_string,',');
    if bool(load_fields):
        request_fields = ArrayUtils.pick(fields, load_fields);
    
    if bool(request_fields) is False:
        request_fields = [fields[0]]
    
    for f in default_fields:
        if f not in request_fields:
            request_fields.append(f);
    
    response = [];
    for f in request_fields:
        response.append(str(f).strip())
    
    return response;

import inspect
def get_class_properties(cls, property='__match_args__'):
        inspected = inspect.getmembers(cls, lambda a:not(inspect.isroutine(a)))
        # attr = [a for a in inspected if not(a[0].startswith('__') and a[0].endswith('__'))]
        attr = [a[1] for a in inspected if a[0]=='__match_args__']
        if(len(attr)>0):
            if type(attr[0]) is tuple:
                return list(attr[0])
        return list(attr)

def get_object_model_class(object_model, cls, fields=None, property='__match_args__'):
        obj = object_model
        attributes = get_class_properties(cls, property);
        if bool(obj) is False:
            obj = {}
            for key in attributes:
                obj[key] = getattr(cls, key, None)

        data_object = DictUtils.pick_object_values(obj, attributes);
        keys = DictUtils.get_keys(data_object);
        if fields is not None:
            for key in attributes:
                if key in fields:
                    if key not in data_object or data_object[key] is None or data_object[key] == 'None':
                        if 'default_value' in fields[key]:
                            data_object[key] = fields[key]['default_value']
        return data_object, attributes

def init_class_kwargs(cls, obj, class_fields, class_fields_props, class_collection_name, ids_key: list[str], **kwargs):
        cls_object, keys = get_object_model_class(obj, cls, class_fields_props);
        kwargs['fields'] = class_fields
        kwargs['fields_props'] = class_fields_props

        for key in ids_key:
            documentId = None;
            if key in cls_object:
                documentId = cls_object[key]
            if documentId is not None and bool(documentId):
                # print('docId', documentId)
                kwargs['id'] = documentId;
                break;
        
        collection_name = getattr(kwargs, 'collection_name', None)
        if collection_name is None or bool(collection_name) is False:
            kwargs['collection_name'] = class_collection_name;
        return cls_object, keys, kwargs;

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        # try:
        #     iterable = iter(obj)
        # except TypeError:
        #     pass
        # else:
        #     return list(iterable)
        # Let the base class default method raise the TypeError
        #return json.JSONEncoder.default(self, obj)
 
       attr = getattr(obj, '__dict__', None)
       if attr is not None:
            return obj.__dict__ 
       return {}

class DateUtils:
    def from_iso(date_str):
        try:
            return date.fromisoformat(date_str);
        except Exception as e:
            return None;
class DictUtils:

    @staticmethod
    def pick_object_values(obj, keys: list[str]):
        cls_object = {};
        for attr in keys:
            cls_object[attr] = pydash.get(obj, attr, None)
        return cls_object
    @staticmethod
    def every_match(element, exceptions=[]):
        if element is None:
            return False;
    
        data = pydash.omit(element, exceptions);
        keys = pydash.keys(data);
        if bool(keys) == False:
            return False;
    
        for key in keys:
            if bool(data[key]) is False:
                print("key", key);
                print("data", data[key]);
                return False;
        return True;

    @staticmethod
    def difference(first_dict, second_dict):
        return { k : second_dict[k] for k in set(second_dict) - set(first_dict) }

    @staticmethod
    def get_changed_field(a, b):
        keys_a = pydash.keys(a);
        keys_b = pydash.keys(b);
        changed_a = [];
        changed_b = [];
        for k in keys_a:
            if a[k]!=b[k]:
                changed_a.append(k);
        
        for k in keys_b:
            if b[k]!=a[k]:
                changed_b.append(k);
        
        changed_fields = pydash.uniq(changed_a + changed_b);
        return changed_fields;

    @staticmethod
    def dict_from_keys(a, keys):
        return pydash.pick(a, keys);

    @staticmethod
    def get_keys(a):
        return pydash.keys(a);
    
    @staticmethod
    def merge_dict(current_dict, target_dict):
        final_dict = target_dict
        for key in pydash.keys(current_dict):
            if key not in final_dict or bool(final_dict[key]) is False or type(current_dict[key])!=type(final_dict[key]) or final_dict[key]!=current_dict[key]:
                final_dict[key] = current_dict[key]
        print('final', final_dict)
        return final_dict;

    @staticmethod
    def string_to_json(element):
        try:
            return json.loads(element);
        except Exception as e:
            print(e)
            return None;
    
    @staticmethod
    def json_to_string(element):
        try:
            return json.dumps(element);
        except:
            return None;

    @staticmethod
    def pick_fields(element, array):
        return pydash.pick(element, array);

    @staticmethod
    def filter(element, keys, path, condition):
        result = {}
        for key in keys:
            if element[key][path] == condition:
                result[key] = element[key]
        return result;
    @staticmethod
    def pick(element, key, data_type, default_value=None):
            if data_type == str:
                if element is not None and key in element:
                    if bool(str(element[key])) is False:
                        if default_value is not None:
                            return default_value
                    return str(element[key]);
                else:
                    if default_value is not None:
                        return default_value
                    return '';
            if data_type == bool:
                if element is not None and key in element:
                    return bool(element[key]);
                else:
                    if default_value is not None:
                        return default_value
                    return False;
    
            if data_type == list:
                if element is not None and key in element:
                    if element[key] is None or bool(list(element[key])) is False:
                        if default_value is not None:
                            return default_value
                        else:
                            return []
                    return list(element[key]);
                else:
                    if default_value is not None:
                        return default_value
                    return [];
            if data_type == dict:
                if element is not None and key in element:
                    if element[key] is not None and bool(dict(element[key])) is False:
                        if default_value is not None:
                            return default_value
                    if element[key] is not None:
                        return dict(element[key]);
                    return None;
                else:
                    if default_value is not None:
                        return default_value
                    return None;
            if data_type == int:
                if element is not None and key in element:
                    return int(element[key]);
                else:
                    if default_value is not None:
                        return default_value
                    return 0;
            if data_type == round:
                if element is not None and key in element:
                    return round(int(str(element[key])));
                else:
                    if default_value is not None:
                        return default_value
                    return 0;
    
            if data_type == float:
                if element is not None and key in element:
                    r = float(str(element[key]))
                    print(f"{key} {r} {type(r)} {element[key]}")
                    if pydash.is_nan(r) or str(r).lower()=='nan':
                        return 0.0
                    return r;
                else:
                    if default_value is not None:
                        return default_value
                    return 0.0;
            return None;

class ArrayUtils:
    @staticmethod
    def filter_array_with_another(array_to_filter, filter):
        return pydash.filter_(array_to_filter, lambda x: pydash.find(filter, lambda y: x==y) is not None);

    @staticmethod
    def get_uniq_value(elements, _key, _key_=None, parse=False):
        keys = [];
        for element in elements:
            if parse is False:
                print('type', type(element[_key]))
                if type(element[_key]) == str or type(element[_key]) == dict:
                    keys.append(element[_key]);
                elif type(element[_key]) == list:
                    keys = pydash.arrays.concat(keys, element[_key])
                    print('here', keys)
            else:
                data = json.loads(JsonEncoder().encode(element))[_key]
                if type(element[_key]) == str or type(element[_key]) == dict:
                    keys.append(data)
                elif type(element[_key]) == list:
                    keys = pydash.arrays.concat(keys, data)
        if _key_ is None:
            return pydash.uniq(keys);
        else:
            return pydash.uniq_by(keys, _key_);
    @staticmethod
    def group_elements_by_key(elements, _key, parse=False):
        keys = ArrayUtils.get_uniq_value(elements, _key, parse);
        result = {};
        for key in keys:
            e = None;
            if parse is False:
                e = pydash.filter_(elements, lambda x: x[_key]==key);
            else:
                e = pydash.filter_(elements, lambda x: json.loads(JsonEncoder().encode(x))[_key]==key);
            if key not in result:
                result[key] = pydash.flatten([e]);
            else:
                result[key] = pydash.flatten(result[key].append(e));
        return result;
    
    @staticmethod
    def sum_grouped_by_key(elements, _key):
        result = []
        for key in pydash.keys(elements):
            sum = pydash.sum_by(elements[key], _key);
            result.append({'key': key, "sum": sum})
        return result;

    @staticmethod
    def string_to_array(element) -> 'list':
        try:
            return json.loads(element);
        except:
            return None;
    
    @staticmethod
    def join_string_to_array(element, separator='') -> 'Iterable[str]':
        try:
            split = str(element).split(separator);
            print('split', split)
            print('element', element);
            if len(split) == 0:
                if len(element) > 0:
                    return [element];
                return []
            else:
                return split;
        except:
            return [];
    
    @staticmethod
    def array_include_array(element, array_check, x = None, y = None) -> 'bool':
        
        def check_filter(check_data, filter_data):
            if x is None or bool(x) is False:
                if y is None or bool(y) is False:
                    return check_data == filter_data
                else:
                    if y in check_data:
                        return check_data[y] == filter_data
                    return False
            else:
                if y is None or bool(y) is False:
                    if x in filter_data:
                        return check_data == filter_data[x]
                    return False
                else:
                    if x in filter_data and y in check_data:
                        return filter_data[x] == check_data[y]
                    return False
                
        def filter(filter_data):
            return pydash.filter_(array_check, lambda arr: check_filter(arr,filter_data))
                 
        return pydash.filter_(element,  lambda element_data: filter(element_data))

    @staticmethod
    def array_to_string(element) -> 'str':
        try:
            return json.dumps(element);
        except:
            return None;
    @staticmethod
    def pick(element, pickable_fields) -> 'list':
        return pydash.filter_(element, lambda x: pydash.includes(pickable_fields, x))
    
    @staticmethod
    def pick_iterable_childs_with_key(iterable, pickable_fields) -> 'list':
        values = [];
        
        if iterable is None or type(iterable) is not list:
            return [];
    
        for element in iterable:
            picked = pydash.pick(element,  pickable_fields);
            if picked is not None and bool(picked) is True:
                values.append(picked);
        return values
    
    @staticmethod
    def pick_iterable_values_with_key(iterable, field) -> 'list':
        values = [];
        
        if iterable is None or type(iterable) is not list:
            return [];
    
        for element in iterable:
            if field in element and bool(element[field]) is True:
                values.append(element[field]);
        return values;

    @staticmethod
    def class_list_to_list_dict(classes):
        values = [];
        for class_object in classes:
            to_json = getattr(class_object, "to_json", None)
            if callable(to_json):
                values.append(class_object.to_json());
        return values;


class RequestUtils:
    @staticmethod
    def get_data(request):
        print(request.data.decode())
        data_request = DictUtils.string_to_json(request.data.decode())
        print("data request",data_request)
        return data_request;