from fastapi import Request
import time

async def global_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(f"Global middleware: {request.method} {request.url} took {process_time}s")
    return response