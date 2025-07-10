from graphql import GraphQLError

class GraphQLHttpError(GraphQLError):
    def __init__(self, message: str, status_code: int):
        super().__init__(message=message, extensions={"status_code": status_code})
