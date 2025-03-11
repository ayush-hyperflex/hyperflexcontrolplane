from fastapi import FastAPI
# from core.plugin_manager import load_module, unload_module, list_installed_modules

import uvicorn
from fastapi import FastAPI
from core.plugin_manager import app, MODULES  # Import app and module list

# API to list installed modules
@app.get("/modules")
def list_installed_modules():
    """Returns the list of currently installed modules."""
    return {"installed_modules": MODULES}

# Entry point for FastAPI application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


