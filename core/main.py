from fastapi import FastAPI
from core.plugin_manager import load_module, unload_module, list_installed_modules

app = FastAPI(title="HyperFlex Control Plane")


@app.get("/modules")
def get_modules():
    """Lists only installed modules."""
    return {"installed_modules": list_installed_modules()}

@app.post("/modules/load/{module_name}")
def load_new_module(module_name: str):
    """Dynamically loads a new module."""
    return {"status": load_module(app, module_name)}

@app.post("/modules/unload/{module_name}")
def unload_existing_module(module_name: str):
    """Dynamically unloads a module."""
    return {"status": unload_module(app, module_name)}
