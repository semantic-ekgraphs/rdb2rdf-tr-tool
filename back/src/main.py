
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .routers import qa, rdb2rdf_routes, stage_1, stage_2, stage_3
from src.constants import TAG_INDEX

from ag_ui_crewai.endpoint import add_crewai_flow_fastapi_endpoint
from src.hitl.hitl import HumanInTheLoopFlow



app = FastAPI()
@app.get("/", tags=[TAG_INDEX], description="Route to Application Home.")
def route_index():
	return {"message": "Hello World! I'm RDB2RDF Incremental View Maintenance Tool!!"}
app.include_router(stage_1.router)
app.include_router(stage_2.router)
app.include_router(stage_3.router)

add_crewai_flow_fastapi_endpoint(
	app=app,
	flow=HumanInTheLoopFlow(),
	path="/human_in_the_loop",
)

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

