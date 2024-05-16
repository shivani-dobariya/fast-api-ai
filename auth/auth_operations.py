import copy

from fastapi import APIRouter, Depends, Request

from database.database import SessionLocal
from database.models.auth_models import User
from database.schemas import SchemaUserCreate, SchemaUserLogin, SchemaUserID
from utils.constants import api_response, provide_all_data, user_created, email_exist, error_msg, login_success, \
    invalid_email, invalid_cred, provide_all_header
from utils.exception_handling import ExceptionHandling
from utils.jwt_authentication.jwt_handler import generate_auth_tokens, JWTBearer, decode_token

auth_router = APIRouter()


@auth_router.post("/signup")
async def signup(user_data: SchemaUserCreate) -> dict:
    # Create a database session
    db = SessionLocal()
    response = copy.deepcopy(api_response)

    try:
        email = user_data.email
        password = user_data.password
        full_name = user_data.full_name

        if not email or not password:
            response.update({
                'error': provide_all_data,
                'message': provide_all_data
            })
            return response
        # Check if username already exists
        user = db.query(User).filter_by(**{'email': email, 'status': 'active'}).first()
        if user:
            response.update({
                'error': email_exist,
                'message': email_exist,
                'status_code': 422
            })
            return response

        # Add the new user to the session and commit to the database
        db.add(User(email=email, password=password, full_name=full_name))

        db.commit()
        response.update({
            'status': True,
            'message': eval(user_created),
            'status_code': 200
        })

    except Exception as e:
        error = ExceptionHandling(e=str(e), function_name='api: /signup').exception_handling(
            message=False)
        response.update({"error": error, "status": False, "message": error_msg})

        return response


    finally:
        db.close()

    return response


@auth_router.post("/login")
async def login(user_data: SchemaUserLogin) -> dict:
    # Create a database session
    db = SessionLocal()
    response = copy.deepcopy(api_response)

    try:
        email = user_data.email
        password = user_data.password

        if not email or not password:
            response.update({
                'error': provide_all_data,
                'message': provide_all_data
            })
            return response

        # Check if email and password  exists
        user = db.query(User).filter_by(**{'email': email, 'password': password, 'status': 'active'}).first()

        # if not user found
        if not user:

            # verify user with email
            user = db.query(User).filter_by(**{'email': email, 'status': 'active'}).first()

            # if user with email found return response with invalid cred
            if not user:
                response.update({
                    'error': invalid_cred,
                    'message': invalid_cred,
                    'status_code': 422
                })

            # else return response with email not exist
            else:
                response.update({
                    'error': invalid_email,
                    'message': invalid_email,
                    'status_code': 422
                })

        else:
            auth_tokens = generate_auth_tokens(user_id=user.id)
            response.update({
                'data': auth_tokens,
                'status': True,
                'error': '',
                'message': login_success,
                'status_code': 200
            })

    except Exception as e:
        error = ExceptionHandling(e=str(e), function_name='api: /login').exception_handling(
            message=False)
        response.update({"error": error, "status": False, "message": error_msg})

        return response

    finally:
        db.close()

    return response


@auth_router.post("/get_user", dependencies=[Depends(JWTBearer())])
async def get_user(user_data: SchemaUserID) -> dict:
    # Create a database session
    db = SessionLocal()
    response = copy.deepcopy(api_response)

    try:
        # Check if email and password  exists
        user = db.query(User).filter_by(**{'id': user_data.id, 'status': 'active'}).first()

        # if not user found
        if not user:

            response.update({
                'error': invalid_email,
                'message': invalid_email,
                'status_code': 422
            })


        else:
            response.update({
                'data': user,
                'status': True,
                'error': '',
                'message': login_success,
                'status_code': 200
            })

    except Exception as e:
        error = ExceptionHandling(e=str(e), function_name='api: /get_user').exception_handling(
            message=False)
        response.update({"error": error, "status": False, "message": error_msg})

        return response

    finally:
        db.close()

    return response


@auth_router.post("/regenerate_token", dependencies=[Depends(JWTBearer())])
async def generate_token(request: Request) -> dict:
    # Create a database session
    db = SessionLocal()
    response = copy.deepcopy(api_response)

    try:
        # List comprehension to filter_by headers containing "authorization"
        matching_headers = [header for header in request.headers.raw if "authorization" in str(header[0]).lower()]

        if matching_headers:
            token = matching_headers[0][1].decode('utf-8').split(' ')[1]

            user_id = decode_token(access_token=token).get('user_id')

            if user_id:
                auth_tokens = generate_auth_tokens(user_id=user_id)
                response.update({
                    'data': auth_tokens,
                    'status': True,
                    'error': '',
                    'message': login_success,
                    'status_code': 200
                })

        else:

            response.update({
                'error': provide_all_header,
                'message': provide_all_header,
                'status_code': 422
            })

    except Exception as e:
        error = ExceptionHandling(e=str(e), function_name='api: /generate_token').exception_handling(
            message=False)
        response.update({"error": error, "status": False, "message": error_msg})

        return response

    finally:
        db.close()

    return response
