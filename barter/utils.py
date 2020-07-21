import json
import math
import os
from django.db import models


def serializer_to_body(serializer, obj, obj_name, context=None):
    data = dict()
    data[obj_name] = serializer(obj).data
    if context:
        data[obj_name] = serializer(obj, context=context).data
    return {'data': data}


def serializer_to_many_body(serializer, objs, objs_name, context=None):
    return {objs_name: serializer(objs, many=True, context=context).data}


def fieldset_serializer_to_body(base_serializer, field_serializer, obj,
                                obj_name, context=None):
    data = dict()
    data[obj_name] = base_serializer(obj).data
    data["fields"] = field_serializer(obj).get_fieldset()
    return {"data": data}


def DictToUrlString(dictionary):
    result = ""
    for key, value in dictionary.items():
        result += str.format("&{}={}", key, value)
    return result


def jsonForm(request):
    return json.loads(request.body.decode('utf-8'))


def post_request_parser(request):
    """
    converts POST requests into appropriate form data:
    json -> form
    form -> form
    """
    if "application/json" in request.META["CONTENT_TYPE"]:
        data = jsonForm(request)
    else:
        data = request.POST.dict()
    return data


def get_type(attribute):
    type_ = type(attribute)
    if type_ == float:
        return "float"
    elif type_ == int:
        return "integer"
    elif type_ == list:
        return "array"
    elif type_ == dict:
        return "object"
    else:
        return "string"


def get_decimal_to_cents(decimal):
    return int(decimal * 100)


class IsActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
