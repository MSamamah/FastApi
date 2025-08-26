from fastapi import Request

async def orders_middleware(request: Request, call_next):
    print("*****This is orders middleware******")
    print(f"Orders middleware: {request.method} {request.url}")
    response = await call_next(request)
    return response