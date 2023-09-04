class AppException(Exception):
    http_status_code = 500


class NotFoundError(AppException):
    http_status_code = 404


class AlreadyExistsError(AppException):
    http_status_code = 409


class DoNotExistsError(AppException):
    http_status_code = 401


class NotActiveError(AppException):
    http_status_code = 401


class AuthenticationError(AppException):
    http_status_code = 401


class SelfCreateUpdateError(AppException):
    http_status_code = 400


class PermissionDeniedError(AppException):
    http_status_code = 403


class BadRequestError(AppException):
    http_status_code = 400


class MultipleRecordsExists(AppException):
    http_status_code = 400
