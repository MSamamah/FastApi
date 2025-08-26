from fastapi import Request
from .registry import registry

async def master_middleware(request: Request, call_next):
    # print(f"helloeeeeeeee {request.url.path}")
    # Get all middlewares for this route
    middlewares = registry.get_middlewares_for_route(request.url.path)
    
    # If no middlewares, just proceed
    if not middlewares:
        return await call_next(request)
    
    # Create a chain of middlewares
    async def apply_middlewares(request, remaining_middlewares):
        if not remaining_middlewares:
            return await call_next(request)
        
        current_middleware = remaining_middlewares[0]
        return await current_middleware(
            request, 
            lambda req: apply_middlewares(req, remaining_middlewares[1:])
        )
    
    return await apply_middlewares(request, middlewares)