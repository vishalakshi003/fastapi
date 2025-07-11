from shared.core.errors.graphql_error import GraphQLHttpError
# from shared.core.response import Response
class HttpError:
    @staticmethod
    def already_exists(details="Data already exists"):
        raise GraphQLHttpError(message=details, status_code=400)

    @staticmethod
    def not_found(details="Data not found"):
        raise GraphQLHttpError(message=details, status_code=404)

    @staticmethod
    def unauthorized(details="You are not authenticated to perform this action!"):
    #     raise GraphQLHttpError(Response(
    #     status="error",
    #     message=details,
    #     status_code=401,
    #     data=None
    # ))
        raise GraphQLHttpError(message=details, status_code=401)

    @staticmethod
    def invalid_mobile_number(details="Invalid mobile number"):
        raise GraphQLHttpError(message=details, status_code=400)

    @staticmethod
    def verify_password(details="Invalid password"):
        raise GraphQLHttpError(message=details, status_code=400)

    @staticmethod
    def exception_handling(details="Something went wrong"):
        raise GraphQLHttpError(message=details, status_code=500)
