from fastapi import Request

async def orders_count_middleware(request: Request, call_next):
    print("*****This is orders count middleware*****")
    print(f"Orders count middleware: {request.method} {request.url}")
    response = await call_next(request)
    return response