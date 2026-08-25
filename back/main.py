from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import qa_routes
from routes import rdb2rdf_routes, r2rml_to_tr_routes


app = FastAPI()
app.include_router(qa_routes.router)
app.include_router(rdb2rdf_routes.router)
app.include_router(r2rml_to_tr_routes.router)

@app.get("/", tags=["Index"])
def route_index():
	return {"message": "Hello World! I'm RDB2RDF Incremental View Maintenance Tool!!"}

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