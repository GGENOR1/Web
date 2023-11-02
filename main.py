import uvicorn
from fastapi import FastAPI
from Controller import handle_startup, handle_shutdown
from router import router

app = FastAPI()


app.include_router(router, tags=["Twidder"], prefix="/main")
app.add_event_handler("startup", handle_startup )
app.add_event_handler("shutdown", handle_shutdown )

if __name__ == "__main__":
    uvicorn.run(app, host = '0.0.0.0', port = 8000)

print("hellow world")