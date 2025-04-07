import os
import importlib
from fastapi import FastAPI
import logging
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Control Plane")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Read available modules from env
MODULES = os.getenv("MODULES", "").split(",")
for module_name in MODULES:
    try:
        # Dynamically import and register module routes
        mod = importlib.import_module(f"modules.{module_name}.routes")
        app.include_router(mod.router, prefix=f"/modules/{module_name}", tags=[module_name])
    except ModuleNotFoundError:
        print(f"Warning: Module '{module_name}' not found in 'modules/' directory.")
