from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import agentic_routes

app = FastAPI()
app.include_router(agentic_routes.router)

origins = [
	"http://localhost:3002",
	"https://localhost.tiangolo.com",
	"http://localhost",
	"http://localhost:8080",
	"http://localhost:5173",
	"http://127.0.0.1:5173",
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
	return {"message": "Hello World, I'm RDB2RDF Tool!!"}