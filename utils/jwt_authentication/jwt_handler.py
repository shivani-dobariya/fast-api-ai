import datetime

import jwt
# The goal of this file is to check whether the reques tis authorized or not [ verification of the proteced route]
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from configurations import AUTH_TOKEN_EXP_MIN, REFRESH_AUTH_TOKEN_EXP_DAY, AUTH_TOKEN_EXP_DAY, \
    REFRESH_AUTH_TOKEN_EXP_MIN, JWT_SECRET_KEY, JWT_ALGORITHUM
from utils.exception_handling import ExceptionHandling


def generate_access_token(user_id):
    """
    function to generate access token
    :param user_id : (int) login user id (e.g. 1)
    :returns:
        binary str: access_token => binary string generated from encrypted user details
    """
    access_token = ''
    try:
        access_token_payload = {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=AUTH_TOKEN_EXP_DAY,
                                                                   minutes=AUTH_TOKEN_EXP_MIN),
        }
        access_token = jwt.encode(access_token_payload,
                                  JWT_SECRET_KEY, algorithm=JWT_ALGORITHUM)

    except Exception as e:
        access_token = ExceptionHandling(e=str(e),
                                         function_name=' function: generate_access_token').exception_handling()

    return access_token


def generate_refresh_token(user_id):
    """
    function to generate refresh access token
    :param user_id : (int) login user user_id (e.g. 1)
    :returns:
        binary str: refresh_token => binary string generated from encrypted user details
    """

    refresh_token = ''
    try:
        refresh_token_payload = {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=REFRESH_AUTH_TOKEN_EXP_DAY,
                                                                   minutes=REFRESH_AUTH_TOKEN_EXP_MIN),
        }
        refresh_token = jwt.encode(
            refresh_token_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHUM)
    except Exception as e:
        refresh_token = ExceptionHandling(e=str(e),
                                          function_name=' function: generate_refresh_token').exception_handling()

    return refresh_token


def generate_auth_tokens(user_id):
    """
    function to generate tokens
    :param user_id : (int) login user id (e.g. 1)
    :returns:
        dict: access_token => binary string generated from encrypted user details, refresh_token => binary string generated from encrypted user details
    """

    access_token = generate_access_token(user_id=user_id)
    refresh_token = generate_refresh_token(user_id=user_id)

    return {'access_token': access_token, 'refresh_token': refresh_token}


def regenerate_access_token(authorization_header):
    """
    function to re-generate tokens based on regeneration token
    :param request : request
    :returns:
        dict: contains access_token => contains binary string generated from encrypted user details, refresh_token => binary string generated from encrypted user details
    """
    access_token = None
    try:
        if not authorization_header:
            return None

        access_token = authorization_header.split(' ')[1]
        payload = jwt.decode(
            access_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHUM], refresh_token=True)

        access_token = generate_auth_tokens(user_id=payload.get('user_id'))

    except Exception as e:
        ExceptionHandling(e=str(e),
                          function_name=' function: regenerate_access_token').exception_handling()
        access_token = None
    return access_token


def decode_token(access_token):
    """
    function to re-generate tokens based on regeneration token
    :param access_token : access_token
    :returns:
        dict: contains access_token => contains binary string generated from encrypted user details, refresh_token => binary string generated from encrypted user details
    """
    try:
        payload = jwt.decode(
            access_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHUM], refresh_token=True)

    except Exception as e:
        ExceptionHandling(e=str(e),
                          function_name=' function: regenerate_access_token').exception_handling()
        payload = None
    return payload


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, access_token: str) -> bool:
        """
        function to verify authentication token
        :param access_token : access_token
        :returns: True if user verified else dict contain detail about error
        """

        try:
            try:
                jwt.decode(
                    access_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHUM])
            except jwt.ExpiredSignatureError:
                print({'error': 'AuthenticationFailed : access_token expired', "status": False, 'status_code': 401})
                return False
            except jwt.InvalidSignatureError:
                print({'error': 'AuthenticationFailed : access_token Invalid', "status": False, 'status_code': 401})
                return False
            return True

        except Exception as e:
            response = ExceptionHandling(e=str(e),
                                         function_name='function: authenticate').exception_handling()

            print({'error': response, "status": False, 'status_code': 401})
            return False
