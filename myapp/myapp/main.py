import asyncio

from fastapi import FastAPI

from myapp.api import router
from myapp.kafka import CONSUMERS, consume_fields
from myapp.fst import rebuilt_fst

app = FastAPI(title='MyApp API')
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_fields())
    asyncio.create_task(rebuilt_fst())


@app.on_event("shutdown")
async def shutdown_event():
    for topics, consumer in CONSUMERS.items():
        await consumer.stop()


@app.get('/')
def get_root():
    return {'message': 'API is running...'}


