__author__ = 'Thibaut Royer'

from .. import app
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, orm, inspect
from flask_sqlalchemy_session import flask_scoped_session


# Handling relationships naming conventions
def _name_for_collection_relationship(base, local_cls, referred_cls, constraint):
    """
    Handler replacement for relationships naming convention
    """
    localname = local_cls.__name__.lower()
    refname = referred_cls.__name__.lower()
    rel_name = None

    if constraint.name:
        rel_name = constraint.name.replace('FK_', '')\
            .replace(refname.upper(), '')\
            .replace(localname.upper(), '')\
            .replace('_', '')
    if rel_name:
        name = localname + "_nREF_" + rel_name + '_' + refname
    else:
        name = localname + "_nREF_" + refname

    print '[DB relationship] ' + name

    return name


def _name_for_scalar_relationship(base, local_cls, referred_cls, constraint):
    """
    Handler replacement for relationships naming convention
    """
    localname = local_cls.__name__.lower()
    refname = referred_cls.__name__.lower()
    rel_name = None

    if constraint.name:
        rel_name = constraint.name.replace('FK_', '')\
            .replace(refname.upper(), '')\
            .replace(localname.upper(), '')\
            .replace('_', '')
    if rel_name:
        name = localname + "_1REF_" + rel_name + '_' + refname
    else:
        name = localname + "_1REF_" + refname

    print '[DB relationship] ' + name

    return name


# Prepare the base reflection and Session
_Base = automap_base()
_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], pool_recycle=3600)
_Base.prepare(_engine, reflect=True,
              name_for_scalar_relationship=_name_for_scalar_relationship,
              name_for_collection_relationship=_name_for_collection_relationship)
orm.configure_mappers()
session_factory = sessionmaker(bind=_engine)

# ------------------------------------------------------------------------------------ #
# ------------------------------ MODIFY HERE ----------------------------------------- #
# ------------------------------------------------------------------------------------ #

# Map the generated classes to proper named objects
# Examples :
# User = _Base.classes.USER
# Type = _Base.classes.TYPE
# State = _Base.classes.STATE

# ------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------ #

# Init the session - get ready to work with !
# Remember to use session.commit() when you finished your work to validate changes.
session = flask_scoped_session(session_factory, app)


# SQL Alchemy weakness : cannot handle uniqueness at recording entry
# Use that function as a fallback
def get_or_create(model, **kwargs):
    """
    Get model instance if already exists or create it.
    Protip: Pass only 'unique' rows, and manipulate your object before commit !
    :param model: DB Entity class
    :param kwargs: Primary key and unique values
    :return: model
    """
    instance = None
    if len(kwargs) > 0:
        instance = session.query(model).filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
    return instance


def secure_add_to_instance(instance, **kwargs):
    """
    Allows to insert data in an SQLAlchemy instance, raising AttributeError if column doesn't exist.
    :param instance: SQLAlchemy instance
    :param kwargs: keywords arguments
    :return: Modified SQLAlchemy instance
    """
    attr_list = inspect(instance).attrs
    for k, v in kwargs.iteritems():
        if k in attr_list:
            setattr(instance, k, v)
        else:
            raise AttributeError
    return instance

