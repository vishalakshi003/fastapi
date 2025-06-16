
from strawberry.extensions import SchemaExtension
from strawberry.types import Info
from typing import Callable, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession

class InjectDBSession(SchemaExtension):
    async def resolve(
        self,
        _next: Callable,
        root: Any,
        info: Info,
        *args,
        **kwargs
    ) -> Any:
        resolver_params = info.field_definition.base_resolver.arguments
        print('resolver_params-------',resolver_params)
        if "db" in resolver_params and "db" not in kwargs:
            db: Optional[AsyncSession] = info.context.get("db")
            if db:
                kwargs["db"] = db

        return await _next(root, info, *args, **kwargs)
