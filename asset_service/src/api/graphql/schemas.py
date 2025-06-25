import strawberry
from .mutations import Mutation
from .queries import Query

from strawberry.federation import Schema
schema = Schema(query=Query, mutation=Mutation)