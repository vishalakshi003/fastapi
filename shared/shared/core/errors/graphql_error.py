from graphql import GraphQLError
from shared.core.response import Response
from typing import TypeVar, Generic

class GraphQLHttpError(GraphQLError):
    def __init__(self, message: str, status_code: int):
        super().__init__(message=message, extensions={"status_code": status_code})

# T = TypeVar("T")

# class GraphQLHttpError(GraphQLError):
#     def __init__(self, data: Response[T]):
#         super().__init__(
#             message=data.message,
#             extensions={
#                 "status": data.status,
#                 "status_code": data.status_code
#             }
#         )