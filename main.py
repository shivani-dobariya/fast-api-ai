from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.auth_operations import auth_router
from configurations import origins
from template_generation.template_operations import template_router

app = FastAPI(debug=True)

#  CORS Configuration


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(template_router, prefix="/templates", tags=["templates"])

# Create database tables
# Base.metadata.create_all(bind=engine)


# Define your FastAPI routes and application logic here

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
