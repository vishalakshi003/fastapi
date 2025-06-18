import strawberry

from src.api.graphql.plugin.database_plugin import InjectDBSession
from .queries import Query
from .mutations import Mutations

schema=strawberry.Schema(query=Query,mutation=Mutations)