from fastapi import FastAPI

from api import crime

app = FastAPI()
app.include_router(crime.router)

