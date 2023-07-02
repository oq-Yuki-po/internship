from fastapi import FastAPI

from app.routers import record_router

APP_TITLE = "Internship FastAPI Sample"
APP_VERSION = "1.0"
APP_DESCRIPTION = "This is a internship FastAPI sample."

app = FastAPI(title=APP_TITLE,
              version=APP_VERSION,
              description=APP_DESCRIPTION)

app.include_router(record_router)


# @app.on_event("startup")
# async def startup_event():
#     initialize_db()
#     initialize_table()
