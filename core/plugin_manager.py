import importlib
from fastapi import FastAPI

installed_modules = set()


def list_installed_modules():
    """Retrieve installed modules"""
    return list(installed_modules)


def load_modules(app: FastAPI):
    """Load installed modules from memory on startup."""
    for module in installed_modules:
        try:
            mod = importlib.import_module(f"modules.{module}.routes")
            app.include_router(mod.router, prefix=f"/{module}", tags=[module])
        except ModuleNotFoundError:
            print(f"Module {module} not found. Skipping...")


def load_module(app: FastAPI, module_name: str):
    """Dynamically install and load a module."""
    if module_name in installed_modules:
        return f"Module {module_name} is already installed."

    try:
        mod = importlib.import_module(f"modules.{module_name}.routes")
        app.include_router(mod.router, prefix=f"/{module_name}", tags=[module_name])
        installed_modules.add(module_name)  # Track installed module in memory
        return f"Module {module_name} installed successfully."
    except ModuleNotFoundError:
        return f"Module {module_name} not found."


def unload_module(app: FastAPI, module_name: str):
    """Dynamically unload a module and remove its routes."""
    if module_name not in installed_modules:
        return f"Module {module_name} was not installed."

    # Remove routes dynamically
    app.router.routes = [
        route for route in app.router.routes if not route.path.startswith(f"/{module_name}")
    ]

    installed_modules.remove(module_name)  # Remove from memory
    return f"Module {module_name} uninstalled successfully."
