from rest_framework.exceptions import APIException


class BadRequest(APIException):
    status_code = 400
    default_detail = 'Your browser sent a request that this server could not understand'
    default_code = 'bad_request'
