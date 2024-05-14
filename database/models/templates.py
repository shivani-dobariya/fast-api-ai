from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database.database import Base


# Define SQLAlchemy models

class TemplatesTypes(Base):
    __tablename__ = "template_types"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, nullable=False, default='active')
    created_on = Column(DateTime, default=datetime.utcnow)
    updated_on = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define relationship with TemplatesParameters table
    templates_list = relationship("Templates", back_populates="template_type")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "templates_list": [template.to_basic_dict() for template in self.templates_list],
            "created_on": self.created_on,
            "updated_on": self.updated_on
        }


class Templates(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, unique=True, nullable=False)
    template_type_id = Column(Integer, ForeignKey('template_types.id'))
    status = Column(String, nullable=False, default='active')
    created_on = Column(DateTime, default=datetime.utcnow)
    updated_on = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define relationship with other table
    template_type = relationship("TemplatesTypes", back_populates="templates_list")
    parameters = relationship("TemplatesParameters", back_populates="parent_template")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "template_type_id": self.template_type_id,
            "template_type": self.template_type.to_dict(),
            "parameters": [param.to_dict() for param in self.parameters],
            "status": self.status,
            "created_on": self.created_on,
            "updated_on": self.updated_on
        }

    def to_basic_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "template_type_id": self.template_type_id,
            "status": self.status,
            "created_on": self.created_on,
            "updated_on": self.updated_on
        }


class TemplatesParameters(Base):
    __tablename__ = "templates_params"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    character_limit = Column(Integer, default=100)
    required = Column(Boolean, unique=True, default=True)
    status = Column(String, nullable=False, default='active')
    template_id = Column(Integer, ForeignKey('templates.id'))
    created_on = Column(DateTime, default=datetime.utcnow)
    updated_on = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define relationship with Templates table
    parent_template = relationship("Templates", back_populates="parameters")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "character_limit": self.character_limit,
            "required": self.required,
            "template_id": self.template_id,
            "status": self.status,
            "created_on": self.created_on,
            "updated_on": self.updated_on
        }
