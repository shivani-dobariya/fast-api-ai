import copy

from fastapi import APIRouter

from configurations import default_chat_completion_model, open_ai
from database.database import SessionLocal, create_db_query
from database.schemas import SchemaTemplates, SchemaTemplatesTypes, SchemaListOfInt, SchemaProcessTemplate
from utils.constants import api_response, no_data, error_msg, success_message
from utils.exception_handling import ExceptionHandling

# dynamically used imports
# from database.models.templates import *
from database.models.templates import *


template_router = APIRouter()


@template_router.post("/template_types")
async def template_list(template_type_id: SchemaListOfInt | None = None) -> dict:
    # Create a database session
    db = SessionLocal()
    response = copy.deepcopy(api_response)

    try:
        filters = {'status': 'active'}
        if template_type_id and template_type_id.id:
            filters.update({'id': template_type_id.id})

        db_query = create_db_query(tb_name='TemplatesTypes', filters=filters)

        # Check if username already exists
        template_types = eval(db_query).all()
        if not template_types:
            response.update({
                'error': no_data,
                'message': no_data,
                'status_code': 200
            })
            return response

        response.update({
            'data': [SchemaTemplatesTypes(**template_type.to_dict()) for template_type in template_types],
            'status': True,
            'message': success_message,
            'status_code': 200
        })

    except Exception as e:
        error = ExceptionHandling(e=str(e), function_name='api: /template_list').exception_handling(
            message=False)
        response.update({"error": error, "status": False, "message": error_msg})

        return response

    finally:
        db.close()

    return response


@template_router.post("/")
async def template_list(template_id: SchemaListOfInt | None = None) -> dict:
    # Create a database session
    db = SessionLocal()
    response = copy.deepcopy(api_response)

    try:
        filters = {'status': 'active'}
        if template_id and template_id.id:
            filters.update({'id': template_id.id})
        db_query = create_db_query(tb_name='Templates', filters=filters)
        templates = eval(db_query).all()
        if not templates:
            response.update({
                'error': no_data,
                'message': no_data,
                'status_code': 200
            })
            return response

        response.update({
            'data': [SchemaTemplates(**template.to_dict()) for template in templates],
            'status': True,
            'message': success_message,
            'status_code': 200
        })

    except Exception as e:
        error = ExceptionHandling(e=str(e), function_name='api: /template_list').exception_handling(
            message=False)
        response.update({"error": error, "status": False, "message": error_msg})

        return response

    finally:
        db.close()

    return response


@template_router.post("/process_template")
async def template_list(template_data: SchemaProcessTemplate) -> dict:
    # Create a database session
    db = SessionLocal()
    response = copy.deepcopy(api_response)

    try:
        filters = {'status': 'active'}
        if template_data and template_data.template_id:
            filters.update({'id': template_data.template_id})
        db_query = create_db_query(tb_name='Templates', filters=filters)
        templates = eval(db_query).first().to_dict()
        query = templates['description'].format(**template_data.parameters)
        content = []
        messages = [{"role": "user", "content": query}]
        for resp in open_ai.chat.completions.create(
                model=default_chat_completion_model,
                messages=messages, stream=True):
            content.append(resp.choices[0].delta.content)

        content = ''.join(content[:-1])
        print(content)

        response.update({
            'data': content,
            'status': True,
            'message': success_message,
            'status_code': 200
        })

    except Exception as e:
        error = ExceptionHandling(e=str(e), function_name='api: /template_list').exception_handling(
            message=False)
        response.update({"error": error, "status": False, "message": error_msg})

        return response

    finally:
        db.close()

    return response
