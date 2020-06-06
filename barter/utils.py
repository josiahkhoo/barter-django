import json
import os


def serializer_to_body(serializer, obj, obj_name):
    data = dict()
    data[obj_name] = serializer(obj).data
    return {'data': data}


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
    if request.META["CONTENT_TYPE"] == "application/json":
        data = jsonForm(request)
    else:
        data = request.POST.dict()
    return data
