from typing import List, Optional

from pydantic import BaseModel


class SchemaUserLogin(BaseModel):
    email: str
    password: str


class SchemaUserCreate(SchemaUserLogin):
    full_name: str


class SchemaUserID(BaseModel):
    id: int


class SchemaUserAll(SchemaUserCreate):
    id: int


class SchemaTemplatesTypesCreate(BaseModel):
    title: str


class SchemaTemplatesBase(BaseModel):
    id: int
    title: str
    description: str
    template_type_id: int


class SchemaTemplatesTypes(SchemaTemplatesTypesCreate):
    id: int
    templates_list: Optional[List[SchemaTemplatesBase]] = None
    status: str

    class Config:
        from_attributes = True


class SchemaTemplatesParametersBase(BaseModel):
    title: str
    character_limit: int
    required: bool
    template_id: int


class SchemaProcessTemplate(BaseModel):
    template_id: int
    parameters: dict


class SchemaTemplatesParametersCreate(SchemaTemplatesParametersBase):
    pass


class SchemaTemplatesParameters(SchemaTemplatesParametersBase):
    id: int
    status: str

    class Config:
        from_attributes = True


class SchemaTemplatesCreate(SchemaTemplatesBase):
    pass


class SchemaTemplates(SchemaTemplatesBase):
    status: str
    template_type: Optional[SchemaTemplatesTypes] = None
    parameters: Optional[List[SchemaTemplatesParameters]] = None

    class Config:
        from_attributes = True


class SchemaListOfInt(BaseModel):
    id: Optional[List[int]] = None
