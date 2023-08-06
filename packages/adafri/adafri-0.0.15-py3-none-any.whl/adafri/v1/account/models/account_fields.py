from dataclasses import dataclass
from  ....utils.utils import DictUtils 

ACCOUNT_COLLECTION = "accounts";

@dataclass
class AccountFields:
    id = "id"
    aacid = "aacid"
    account_value = "account_value"
    creationDate = "creationDate"
    creationDateString = "creationDateString"
    name = "name"
    owner = "owner"
    owner_email = "owner_email"
    status = "status"
    totalClics = "totalClics"
    totalCosts = "totalCosts"
    totalImpressions = "totalImpressions"
    usedPackTest = "usedPackTest"

    @staticmethod
    def keys():
        return DictUtils.get_keys(AccountFieldProps);

    @staticmethod
    def filtered_keys(field, condition=True):
        mutable = DictUtils.filter(AccountFieldProps, DictUtils.get_keys(AccountFieldProps), field, condition)
        return DictUtils.get_keys(mutable);



AccountFieldProps = {
    AccountFields.id: {
        "type": str,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": ""
    },
    AccountFields.aacid: {
        "type": str,
        "required": True,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": ""
    },
    AccountFields.account_value: {
        "type": (int or float),
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": 0
    },
    AccountFields.creationDateString: {
        "type": str,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": False,
        "pickable": True,
        "default_value": ""
    },
    AccountFields.creationDate: {
        "type": str,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": ""
    },
    AccountFields.name: {
        "type": str,
        "required": True,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": ""
    },
    AccountFields.owner: {
        "type": str,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": ""
    },
    AccountFields.owner_email: {
        "type": str,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": ""
    },
    AccountFields.status: {
        "type": str,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": ""
    },
    AccountFields.totalClics: {
        "type": str,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": ""
    },
    AccountFields.totalCosts: {
        "type": str,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": ""
    },
    AccountFields.totalImpressions: {
        "type": str,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": ""
    },
    AccountFields.usedPackTest: {
        "type": bool,
        "required": False,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": False
    }


}

STANDARD_FIELDS = AccountFields.filtered_keys('pickable', True)
