import copy

from fastapi import APIRouter

from database.database import SessionLocal
from database.models.auth_models import User
from database.schemas import UserCreate, UserLogin
from utils.constants import api_response, provide_all_data, user_created, email_exist, error_msg, login_success, \
    invalid_email, invalid_cred
from utils.exception_handling import ExceptionHandling

auth_router = APIRouter()


@auth_router.post("/signup")
def signup(user_data: UserCreate):
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
        user = db.query(User).filter(User.email == email, User.status == 'active').first()
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
        error = ExceptionHandling(e=str(e), function_name=f'api: /signup').exception_handling(
            message=False)
        response.update({"error": error, "status": False, "message": error_msg})

        return response


    finally:
        db.close()

    return response


@auth_router.post("/login")
def login(user_data: UserLogin):
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
        user = db.query(User).filter(User.email == email, User.password == password, User.status == 'active').first()

        # if not user found
        if not user:

            # verify user with email
            user = db.query(User).filter(User.email == email, User.status == 'active').first()

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
            response.update({
                'status': True,
                'error': '',
                'message': login_success,
                'status_code': 200
            })

    except Exception as e:
        error = ExceptionHandling(e=str(e), function_name=f'api: /login').exception_handling(
            message=False)
        response.update({"error": error, "status": False, "message": error_msg})

        return response


    finally:
        db.close()

    return response
