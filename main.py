from fastapi import FastAPI

from auth.auth_operations import auth_router
from templates.template_operations import template_router

app = FastAPI(debug=True)

# Mount routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(template_router, prefix="/template", tags=["template"])

# Create database tables
# Base.metadata.create_all(bind=engine)


# Define your FastAPI routes and application logic here

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
