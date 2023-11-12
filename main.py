import uvicorn
from fastapi import FastAPI
from Connection.Controller import handle_startup, handle_shutdown
from router import router

app = FastAPI()


app.include_router(router, tags=["Twidder"], prefix="/main")
app.add_event_handler("startup", handle_startup )
app.add_event_handler("shutdown", handle_shutdown )

print("hellow world")