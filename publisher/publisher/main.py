import time

from fastapi import Depends, FastAPI, Request

from publisher.dependencies import get_kafka_producer
from publisher.views import v1


app = FastAPI(title='Kafka Publisher API')
app.include_router(v1.router, prefix="/v1", tags=["v1"], dependencies=[Depends(get_kafka_producer)])

kafka_producer = get_kafka_producer()


@app.on_event("startup")
async def startup_event():
    await kafka_producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await kafka_producer.stop()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get('/')
def get_root():
    return {'message': 'API is running...'}


