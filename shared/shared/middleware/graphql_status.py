from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import json
from starlette.concurrency import iterate_in_threadpool

class ForceGraphQLHTTPStatusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        if request.url.path.startswith("/graphql") and request.method == "POST":
            body = b""
            async for chunk in response.body_iterator:
                body += chunk

            response.body_iterator = iterate_in_threadpool([body])

            try:
                json_body = json.loads(body)
                if "errors" in json_body:
                    err = json_body["errors"][0]
                    extensions = err.get("extensions", {})
                    status = extensions.get("status_code", 400)
                    response.status_code = status
            except json.JSONDecodeError:
                pass

        return response
