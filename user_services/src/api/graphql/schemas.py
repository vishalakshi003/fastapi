import strawberry

from src.api.graphql.plugin.database_plugin import InjectDBSession
from src.api.graphql.types import User
from .queries import Query
# from .mutations import Mutations
from .user import Mutation
from strawberry.federation import Schema

schema=Schema(query=Query,mutation=Mutation,types=[User])