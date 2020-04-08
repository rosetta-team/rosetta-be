import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .models import db_session, Language as LanguageModel, Method as MethodModel

class Method(SQLAlchemyObjectType):
    class Meta:
        model = MethodModel
        interfaces = (relay.Node, )

class Language(SQLAlchemyObjectType):
    class Meta:
        model = LanguageModel
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_languages = SQLAlchemyConnectionField(Language.connection)
    all_methods = SQLAlchemyConnectionField(Method.connection)

schema = graphene.Schema(query=Query)