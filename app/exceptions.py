from fastapi import HTTPException, status


class UserException(HTTPException):
    status_code = 500
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(UserException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'User already exists'


class IncorrectEmailOrPasswordException(UserException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Incorrect Email or Password'


class TokenExpiredException(UserException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Token has been expired'


class NoTokenException(UserException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'No token'


class IncorrectFormatTokenException(UserException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Incorrect token format'


class NoUserException(UserException):
    status_code = status.HTTP_401_UNAUTHORIZED


class CurException(HTTPException):
    status_code = 500
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class WrongCurrencyLen(CurException):
    status_code = 400
    detail = 'Length must be 3 characters'


class NoSuchCurException(CurException):
    status_code = 404
    detail = 'No such currency'


class WrongAmountException(CurException):
    status_code = 409
    detail = 'Amount must be greater then 0'
