import strawberry

from src.api.graphql.plugin.database_plugin import InjectDBSession
from src.api.graphql.types import User
from .queries import Query
from .mutations import Mutations
from strawberry.federation import Schema

schema=Schema(query=Query,mutation=Mutations,types=[User])